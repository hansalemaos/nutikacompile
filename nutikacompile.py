import itertools
import os
import subprocess
import sys
import tempfile
from typing import Union, Tuple

from FastCopyFast import copyfile
from PIL import Image
from touchtouch import touch


def iter_find_same_beginning_elements(iters):
    return (x[0] for x in itertools.takewhile(lambda x: len(set(x)) == 1, zip(*iters)))


def find_same_common_folder(files):
    samebe = "".join(
        list(
            iter_find_same_beginning_elements(
                [x.folder if hasattr(x, "folder") else x for x in files + files]
            )
        )
    )
    while not os.path.isdir(samebe) and not os.path.ismount(samebe):
        samebe = os.sep.join(samebe.split(os.sep)[:-1])
        if not samebe:
            return ""
    return samebe


def tempfolder():
    tempfolder = tempfile.TemporaryDirectory()
    tempfolder.cleanup()
    if not os.path.exists(tempfolder.name):
        os.makedirs(tempfolder.name)

    return tempfolder.name


def copy_folder_to_another_folder(
    files: list,
) -> Tuple[str, list]:
    r"""
    Copies all files and folders from the source folder to the destination folder.
    If the destination folder is not specified, a temporary folder is created.
    Only files with allowed extensions are copied if specified.
    The maximum number of subfolders to copy can be specified.
    Args:
    - src (str): The path of the source folder to copy from.
    - dest (Union[str, None], optional): The path of the destination folder to copy to. Defaults to None.
    - allowed_extensions (tuple, optional): A tuple of allowed file extensions to copy. Defaults to () (all files allowed).
    - maxsubfolders (int, optional): The maximum number of subfolders to copy. Defaults to -1 (all subfolders).
    Returns:
    - Tuple[str, list]: A tuple containing the path of the destination folder and a list of tuples.
    Each tuple in the list contains a boolean value indicating whether the file was successfully copied and the path of the copied file.
    """
    temp_package_path = tempfolder()

    files = [os.path.normpath(x) for x in files]
    samebe = find_same_common_folder(files)
    samebe.rstrip(os.sep)
    results = []
    for e in files:
        old = e
        new = os.path.normpath(
            os.path.join(temp_package_path, e[len(samebe) :].lstrip(os.sep))
        )
        touch(new)
        if os.path.isdir(new):
            os.rmdir(new)
        elif os.path.isfile(new):
            os.remove(new)
        try:
            copyfile(old, new)
            results.append((True, new))
        except Exception as fe:
            print(fe)
            results.append((False, new))
    return temp_package_path, results


def create_icon(filename, iconfilename):
    img = Image.open(filename)
    img.save(iconfilename)


def get_tmpfile(suffix=".ico"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    touch(filename)
    return filename


def compile_with_nuitka(
    pyfile: str,
    icon: Union[str, None] = None,
    disable_console: bool = True,
    onefile: bool = True,
    file_version: str = "1",
    file_description: str = "",
    product_name: str = "",
    copyright: str = "",
    trademarks: str = "",
    outputdir: Union[str, None] = None,
    addfiles: Union[list, None] = None,
    delete_onefile_temp: bool = False,
    needs_admin: bool = False,
    relativefolderinapps: Union[None, str] = None,
    arguments2add: str = "",
) -> str:
    """
    Compiles a Python file using Nuitka.

    Args:
        pyfile (str): The path to the Python file to be compiled.
        icon (Union[str, None], optional): The path to the icon file to be used for the compiled executable. Defaults to None.
        disable_console (bool, optional): Whether to disable the console window for the compiled executable. Defaults to True.
        onefile (bool, optional): Whether to create a single executable file. Defaults to True.
        file_version (str, optional): The version number to be assigned to the compiled executable. Defaults to "1".
        outputdir (Union[str, None], optional): The path to the directory where the compiled executable will be saved. Defaults to None.
        addfiles (Union[list, None], optional): A list of files to be included in the compiled executable. Defaults to None.
        delete_onefile_temp (bool, optional): Whether to delete the temporary directory for the single executable file. Defaults to False.
        needs_admin (bool, optional): Whether the compiled executable requires administrative privileges to run. Defaults to False.
        relativefolderinapps (Union[None, str], optional): The relative folder path to be used for the compiled executable. Defaults to None.
        arguments2add (str, optional): Additional arguments to be passed to the Nuitka compiler. Defaults to "".

    Returns:
        str: The command used to compile the Python file.
    """
    addtocmd = ""

    if outputdir:
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)
        outputdirp = os.path.normpath(outputdir).replace("\\", "/")
        addtocmd = addtocmd + f" --output-dir={outputdirp}"
    if disable_console:
        addtocmd = addtocmd + " --windows-disable-console"
    if onefile:
        addtocmd = addtocmd + " --onefile"
    if icon:
        iconfilename = get_tmpfile(suffix=".ico")
        create_icon(icon, iconfilename)
        iconfilename = iconfilename.replace("\\", "/")
        addtocmd = addtocmd + f" --windows-icon-from-ico={iconfilename}"
    if addfiles:
        fi = copy_folder_to_another_folder(addfiles)
        foldercommand = (
            " --include-data-files=" + fi[0].replace("\\", "/") + "=.//=**/*.*"
        )
        addtocmd = addtocmd + foldercommand
    if needs_admin:
        addtocmd = addtocmd + " --windows-uac-admin"

    addtocmd = addtocmd + f" --file-version={file_version}"
    addtocmd = addtocmd + f' --product-name="{product_name}"'
    addtocmd = addtocmd + f' --file-description="{file_description}"'
    addtocmd = addtocmd + f' --copyright="{copyright}"'
    addtocmd = addtocmd + f' --trademarks="{trademarks}"'

    if not delete_onefile_temp:
        if not relativefolderinapps:
            basename = ".".join(os.path.basename(pyfile).split(".")[:-1])
        else:
            basename = relativefolderinapps.strip('\\" ')
        cdi = f"%CACHE_DIR%/{basename}/{file_version}"
        addtocmd = addtocmd + f" --onefile-tempdir-spec={cdi}"
    if arguments2add:
        addtocmd = addtocmd + " " + arguments2add.strip()
    backs = "\\"
    forw = "/"
    wholecommand = (
        f'start "" "{sys.executable}" -m nuitka {pyfile.replace(backs, forw)} --standalone --assume-yes-for-downloads'
        + addtocmd
    )
    p = subprocess.Popen(wholecommand, shell=True)

    return wholecommand

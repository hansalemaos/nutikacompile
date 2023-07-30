# A function that creates the cmd line for nuitka and executes it 

update:
Added executable properties description
This information is useful in some scenarios, such as notifications

```python
pip install nutikacompile
```

```python
from nutikacompile import compile_with_nuitka
# creates the command line and executes it in a new console
wholecommand = compile_with_nuitka(
    pyfile=r"C:\ProgramData\anaconda3\envs\adda\secretsubprocess.py",
    icon=r"C:\Users\hansc\Pictures\radiobutton.png",
    disable_console=True,
    file_version="1.0.0.0",
    file_description="My App",
    product_name="My app that do something",
    copyright="(c) Acme",
    trademarks="(c) Acme LTDA",
    onefile=True,
    outputdir="c:\\compiledapptest",
    addfiles=[
        r"C:\ProgramData\anaconda3\envs\adda\convertpic2ico.exe",  # output: compiledapptest/convertpic2ico.exe
        r"C:\ProgramData\anaconda3\envs\adda\pi2\README.MD",  # output: compiledapptest/pi2/README.MD
    ],
    delete_onefile_temp=False,  # creates a permanent cache folder
    needs_admin=True,
)
print(wholecommand)

# The function creates and executes this command: 
start "" "C:\ProgramData\anaconda3\envs\adda\python.exe" -m nuitka C:/ProgramData/anaconda3/envs/adda/secretsubprocess.py --assume-yes-for-downloads --output-dir=c:/compiledapptest --windows-disable-console --onefile --windows-icon-from-ico=C:/Users/hansc/AppData/Local/Temp/tmpb4w1z8d9.ico --include-data-files=C:/Users/hansc/AppData/Local/Temp/tmpb4i48w8_=.//=**/*.* --windows-uac-admin --file-version=1.0.0.0 --onefile-tempdir-spec=%CACHE_DIR%/nutikacompile/1.0.0.0


compile_with_nuitka(
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
) -> str
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
```

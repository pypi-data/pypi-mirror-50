# startkit

A skeleton generator for python projects.

## Installation
```cmd
pip install startkit
```

## Demo
```cmd
cd C:\workspace (workspace)
startkit

> Create the project under which path [C:\workspace]?
> Please enter your project name [myproject]:
> Please enter main package name [myproject]:
> Please enter your project version [0.0.1]:
> Please enter your project description:demo
> Please enter your name [***]:******
> Please enter your email:******@***.com
The project has been successfully created!

cd myproject
python -m venv venv
venv\Scripts\activate.bat (cmd.exe)
venv\Scripts\Activate.ps1 (PowerShell)
source venv/bin/activate (bash/zsh)
pip install -r requirements.txt
pip freeze > requirements.txt
python -m myproject (package name)
...
deactivate
```

**warning**: The text in "()" is just explanatory text. Don't paste them to run.

**warning**: For more executable commands, refer to the "Makefile" file.

## Bug Reports
If you have any bugs to report, you're welcome to file an [issue](https://github.com/niemingzhao/startkit/issues).

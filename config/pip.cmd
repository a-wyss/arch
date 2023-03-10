@echo off
set ini=%appdata%\pip\pip.ini
if not exist %ini%\..\ (
    mkdir %ini%\..\
)
echo [global]>%ini%
echo trusted-host = pypi.python.org>>%ini%
echo                pypi.org>>%ini%
echo                files.pythonhosted.org>>%ini%
echo Successfully created %ini%
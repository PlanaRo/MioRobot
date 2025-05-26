@echo off
setlocal enabledelayedexpansion

for /F %%i in ('where python') do (
    set "PYTHON_PATH=%%i"
    if defined PYTHON_PATH (
	pip install -r requirements.txt
        !PYTHON_PATH! main.py
	goto :eof
    ) else (
	set "url=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
	set "filename=python-3.11.9-amd64.exe"
	set "destination_folder=%ProgramFiles%\Python311"

	echo Download Python...
	curl -o "%filename%" "%url%"

	if %errorlevel% neq 0 (
    	echo Download failed, please check your network connection or download link.
    	pause
    	exit /b 1
	)

	echo Installing Python...
	%filename% InstallAllUsers=1 PrependPath=1 TargetDir="%destination_folder%"

	if %errorlevel% neq 0 (
    	echo Installation failed, please check the installer.
    	pause
    	exit /b 1
	)

	python -m pip -V
	pip install -r requirements.txt
         "%destination_folder%\python.exe" main.py
    )
)
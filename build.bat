@echo off
setlocal enabledelayedexpansion

REM Determine important paths
set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
set "VENV_DIR=%PROJECT_ROOT%\.venv-build"
set "SPEC_FILE=%PROJECT_ROOT%\packaging\app.spec"

if not exist "%SPEC_FILE%" (
    echo [ERROR] Unable to locate %%SPEC_FILE%%: %SPEC_FILE%
    exit /b 1
)

if exist "%VENV_DIR%" (
    echo Removing existing virtual environment...
    rmdir /s /q "%VENV_DIR%"
)

echo Creating temporary virtual environment...
python -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    exit /b 1
)

call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Unable to activate virtual environment.
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 goto build_error

if exist "%PROJECT_ROOT%\requirements.txt" (
    echo Installing project requirements...
    pip install -r "%PROJECT_ROOT%\requirements.txt"
    if errorlevel 1 goto build_error
) else (
    echo requirements.txt not found. Installing PyInstaller directly.
    pip install pyinstaller
    if errorlevel 1 goto build_error
)

echo Running PyInstaller build...
pyinstaller "%SPEC_FILE%" --noconfirm --clean
if errorlevel 1 goto build_error

echo Build completed successfully.
echo Output available in: %PROJECT_ROOT%\dist

goto build_end

:build_error
echo [ERROR] Build failed with exit code %errorlevel%.
exit /b %errorlevel%

:build_end
endlocal

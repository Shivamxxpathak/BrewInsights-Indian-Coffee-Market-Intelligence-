@echo off
setlocal
cd /d "%~dp0"

title Coffee Market Dashboard

echo ==============================================
echo       COFFEE MARKET DASHBOARD
echo ==============================================
echo.

set "APP=%~dp0dashboard\app.py"
set "REQ=%~dp0requirements_dashboard.txt"
set "PY=%LocalAppData%\Python\pythoncore-3.14-64\python.exe"

if not exist "%APP%" (
    echo [ERROR] dashboard\app.py not found.
    echo Make sure this BAT file is in the main project folder.
    echo.
    pause
    exit /b 1
)

rem Find Python automatically if the configured path is not available.
if exist "%PY%" goto PYTHON_READY

where py >nul 2>&1
if not errorlevel 1 (
    set "PY=py -3"
    goto PYTHON_READY
)

where python >nul 2>&1
if not errorlevel 1 (
    set "PY=python"
    goto PYTHON_READY
)

echo [ERROR] Python could not be found.
echo Please install Python and try again.
echo.
pause
exit /b 1

:PYTHON_READY
echo Checking Streamlit and required packages...
%PY% -c "import streamlit, pandas, numpy, plotly, sklearn" >nul 2>&1

if errorlevel 1 (
    echo Required packages are missing. Installing them now...
    echo.
    %PY% -m pip install -r "%REQ%"
    if errorlevel 1 (
        echo.
        echo [ERROR] Package installation failed.
        pause
        exit /b 1
    )
)

echo.
echo Starting Streamlit dashboard...
echo Your browser should open automatically.
echo.

%PY% -m streamlit run "%APP%" --server.headless false

if errorlevel 1 (
    echo.
    echo [ERROR] Dashboard stopped with an error.
)

pause

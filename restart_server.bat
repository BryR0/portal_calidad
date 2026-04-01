@echo off
setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

for %%I in ("%SCRIPT_DIR%.") do set PROJECT_NAME=%%~nxI

set PROJECT_RUN_PATH=%SCRIPT_DIR%run.py
set SHARED_VENV_PYTHON=%SCRIPT_DIR%venv\Scripts\python.exe


echo Limpiando cache y reiniciando servidor...
echo.

echo Buscando procesos que contengan: %PROJECT_NAME%

set "PIDS="

for /f %%P in ('
    powershell -NoProfile -Command "$p='%SCRIPT_DIR%'; $self=$PID; Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -ne $self -and ($_.Name -eq 'python.exe' -or $_.Name -eq 'pythonw.exe') -and $_.CommandLine -like ('*' + $p + '*') } | Select-Object -ExpandProperty ProcessId" 2^>nul
') do (
    set "PIDS=!PIDS! %%P"
)

if defined PIDS (
    echo Deteniendo procesos:%PIDS%
    for %%p in (%PIDS%) do (
        taskkill /PID %%p /F >nul 2^>^&1
    )
) else (
    echo No se encontraron procesos activos de %PROJECT_NAME%.
)

echo Limpiando __pycache__...


for /d /r %%d in (__pycache__) do (
    if exist "%%d" rd /s /q "%%d"
)

del /s /q *.pyc >nul 2>&1

echo Generando tailwind...

set TAILWIND_INPUT=%SCRIPT_DIR%app\static\css\input.css
set TAILWIND_OUTPUT=%SCRIPT_DIR%app\static\css\tailwind.css

call npx tailwindcss -i "%TAILWIND_INPUT%" -o "%TAILWIND_OUTPUT%" --minify

if errorlevel 1 (
    echo Error generando tailwind.css
    exit /b 1
)

echo Cache limpiado. Iniciando servidor...
echo.

if exist "%SHARED_VENV_PYTHON%" (
    "%SHARED_VENV_PYTHON%" "%PROJECT_RUN_PATH%"
    exit /b
)

if exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
    "%SCRIPT_DIR%.venv\Scripts\python.exe" "%PROJECT_RUN_PATH%"
    exit /b
)

if exist "%SCRIPT_DIR%venv\Scripts\python.exe" (
    "%SCRIPT_DIR%venv\Scripts\python.exe" "%PROJECT_RUN_PATH%"
    exit /b
)

where python >nul 2>&1
if %errorlevel%==0 (
    python "%PROJECT_RUN_PATH%"
    exit /b
)

where python3 >nul 2>&1
if %errorlevel%==0 (
    python3 "%PROJECT_RUN_PATH%"
    exit /b
)

python "%PROJECT_RUN_PATH%"

@echo off
:: Install dependencies with 'python -m'
echo Installing dependencies using 'python -m pip'...
python -m pip install -r requirements.txt

:: Check if the installation was successful
if %errorlevel% neq 0 (
    echo Installation using 'python -m pip' failed. Retrying without 'python -m'...
    pip install -r requirements.txt

    :: Check if the installation was successful
    if %errorlevel% neq 0 (
        echo Installation failed. Please check the error messages above.
    ) else (
        echo Installation completed successfully.
    )
) else (
    echo Installation completed successfully.
)

echo Press any key to close...
pause >nul

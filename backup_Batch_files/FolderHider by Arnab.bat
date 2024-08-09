@echo off

cd APP
python Terminal.py
if %errorlevel% neq 0 (
    powershell -command "Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('An error occurred while running Terminal.py', 'Error', 'OK', 'Error')"
)


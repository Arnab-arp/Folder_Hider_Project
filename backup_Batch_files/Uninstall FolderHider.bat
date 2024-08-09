@echo off

echo FolderHider by Arnab...
echo (This project is Created and maintained by Arnab Pramanik. All rights reserved.)
echo For More Info, Visit:
echo Github: https://github.com/Arnab-arp

timeout /t 5

where python >nul 2>&1
if %errorlevel% == 0 (
	cls
	
	echo Python is installed.
    	echo Uninstalling Packages....
	
	timeout /t 3 /nobreak
	
    	pip uninstall -y pycryptodome
    	pip uninstall -y tk-tools
	pip uninstall -y tqdm
	pip uninstall -y FDH_Library-1.0-py3-none-any.whl
	
	cd APP
	attrib -h -s -r "secrets.cdf5"
	if exist "Error Logs.log" del "Error Logs.log" 
	if exist "secrets.cdf5" del "secrets.cdf5"
	echo --------------------------------------------------------------------------------------------
	echo All Packages Uninstalled Successfully!
	echo Safe To Delete The Project Folder

) else (
	echo Python is not installed.
	echo Please install Python before running this program again. 
)
pause

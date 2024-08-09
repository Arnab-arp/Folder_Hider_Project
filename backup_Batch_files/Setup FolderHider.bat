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
    	echo Installing Necessary Packages ....
	
	timeout /t 3
	
	python.exe -m pip install --upgrade pip
    	pip install pycryptodome
    	pip install tk-tools
	pip install tqdm

	cd dist

	pip install FDH_Library-1.0-py3-none-any.whl

	echo --------------------------------------------------------------------------------------------	
	echo All Packages Installed Successfully!

) else (
	echo Python is not installed.
	echo Please install Python before running this program again. 
)
pause

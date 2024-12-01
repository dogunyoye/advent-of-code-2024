@echo off

::=================================================================
:: This script creates a Python directory (module) for a specific
:: day, with some simple bolierplate code in the python source file
::
:: Usage:
::     aoc_helper.bat day01
::
:: Output:
::     Created folder C:\Users\Dimeji\day01
::     Created file C:\Users\Dimeji\day01.py
::     Created file C:\Users\Dimeji\day01\__init__.py
::=================================================================

if not exist "%__CD__%\%1" ( goto :created ) else ( goto :exists )

:exists
    echo Folder already exists. Exiting..
    goto :eof
	
:created
	echo Created folder %__CD__%%1
	mkdir %__CD__%%1

(
echo import os.path
echo.
echo DATA = os.path.join(os.path.dirname(__file__^), '%1.txt'^)
echo.
echo.
echo def main(^) -^> int:
echo 	with open(DATA^) as f:
echo 		data = f.read(^)
echo 	return 0
echo.
echo.
echo if __name__ == '__main__':
echo 	raise SystemExit(main(^)^)
echo.
)>%__CD__%%1\%1.py
echo Created file %__CD__%%1.py

type nul >%__CD__%%1\__init__.py
echo Created file %__CD__%%1\__init__.py

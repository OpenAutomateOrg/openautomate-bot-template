@echo off
setlocal enabledelayedexpansion

echo ========================================
echo OpenAutomate Bot Builder
echo ========================================

:: Check if bot.json exists
if not exist "bot.json" (
    echo ERROR: bot.json not found!
    echo Please make sure you're running this from the bot directory.
    pause
    exit /b 1
)

:: Read current version from bot.json
for /f "tokens=2 delims=:, " %%a in ('findstr "version" bot.json') do (
    set version_line=%%a
    set version_line=!version_line:"=!
    set current_version=!version_line!
)

echo Current version: %current_version%

:: Parse version (assuming format x.y.z)
for /f "tokens=1,2,3 delims=." %%a in ("%current_version%") do (
    set major=%%a
    set minor=%%b
    set patch=%%c
)

:: Increment patch version
set /a patch+=1
set new_version=%major%.%minor%.%patch%

echo New version: %new_version%

:: Update bot.json with new version
powershell -Command "(Get-Content bot.json) -replace '\"version\": \"%current_version%\"', '\"version\": \"%new_version%\"' | Set-Content bot.json"

:: Sync metadata from bot.json to config.ini
echo Syncing metadata...
powershell -ExecutionPolicy Bypass -File "sync-metadata.ps1"

:: Read bot name from bot.json
for /f "tokens=2 delims=:, " %%a in ('findstr "name" bot.json') do (
    set name_line=%%a
    set name_line=!name_line:"=!
    set bot_name=!name_line!
)

:: Clean bot name for filename (replace spaces with underscores, remove special chars)
set clean_name=%bot_name: =_%
set clean_name=%clean_name:(=%
set clean_name=%clean_name:)=%
set clean_name=%clean_name:[=%
set clean_name=%clean_name:]=%

:: Create output filename
set output_file=%clean_name%.%new_version%.zip

echo Building package: %output_file%

:: Create temporary build directory
if exist "build_temp" rmdir /s /q "build_temp"
mkdir "build_temp"

:: Copy files to build directory (exclude build artifacts and git files)
xcopy "*.py" "build_temp\" /y >nul
xcopy "*.json" "build_temp\" /y >nul
xcopy "*.txt" "build_temp\" /y >nul
xcopy "*.md" "build_temp\" /y >nul
if exist "config" xcopy "config" "build_temp\config\" /e /y >nul
if exist "framework" xcopy "framework" "build_temp\framework\" /e /y >nul
if exist "examples" xcopy "examples" "build_temp\examples\" /e /y >nul
if exist "tasks" xcopy "tasks" "build_temp\tasks\" /e /y >nul

:: Create ZIP file using PowerShell
powershell -Command "Compress-Archive -Path 'build_temp\*' -DestinationPath '%output_file%' -Force"

:: Clean up
rmdir /s /q "build_temp"

if exist "%output_file%" (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo Package: %output_file%
    echo Version: %new_version%
    echo.
    echo You can now upload this package to OpenAutomate.
    echo ========================================
) else (
    echo.
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo Could not create package file.
)

pause 
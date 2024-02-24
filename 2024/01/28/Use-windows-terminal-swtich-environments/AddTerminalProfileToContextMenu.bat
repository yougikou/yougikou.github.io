@echo off
set /p ProfileName="Enter the Windows Terminal profile name: "
set /p IconPath="Enter the full path to the icon file (e.g., C:\\path\\to\\icon.ico), or press Enter to use the default CMD icon: "

:: 如果未输入图标路径，使用 CMD 的默认图标
if "%IconPath%"=="" set IconPath=%SystemRoot%\System32\cmd.exe

:: 将单斜杠替换为双斜杠
set IconPath=%IconPath:\=\\%

:: 创建 .reg 文件
>AddTerminalProfile.reg echo Windows Registry Editor Version 5.00
>>AddTerminalProfile.reg echo.
>>AddTerminalProfile.reg echo [HKEY_CLASSES_ROOT\Directory\Background\shell\Open Terminal %ProfileName%]
>>AddTerminalProfile.reg echo @="Open Terminal %ProfileName%"
>>AddTerminalProfile.reg echo "Icon"="%IconPath%"
>>AddTerminalProfile.reg echo.
>>AddTerminalProfile.reg echo [HKEY_CLASSES_ROOT\Directory\Background\shell\Open Terminal %ProfileName%\command]
>>AddTerminalProfile.reg echo @="wt.exe -p \"%ProfileName%\""

:: 导入 .reg 文件
reg import AddTerminalProfile.reg

if %errorlevel% neq 0 (
    echo Failed to update the registry. Please run as administrator.
) else (
    echo Successfully added to the context menu.
)

pause

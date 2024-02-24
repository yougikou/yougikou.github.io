@echo off
SETLOCAL EnableDelayedExpansion

:: 初始化变量
set "hasProfiles=0"

:: 列出所有以 "Open Terminal" 开头的注册表项
echo Available profiles to remove:
for /f "tokens=3*" %%a in ('reg query "HKEY_CLASSES_ROOT\Directory\Background\shell" 2^>nul ^| find "Open Terminal"') do (
  set "hasProfiles=1"
  echo - %%a
)

:: 检查是否找到了配置文件
if "!hasProfiles!"=="0" (
  echo No 'Open Terminal' profiles found in the context menu.
  pause
  exit /b
)

:: 提示用户输入要删除的配置文件名
set /p ProfileName="Enter the profile name to remove (exactly as listed above): "

:: 检查用户输入是否为空
if "!ProfileName!"=="" (
    echo No profile name entered. Exiting.
    exit /b
)

:: 删除注册表项
reg delete "HKEY_CLASSES_ROOT\Directory\Background\shell\Open Terminal !ProfileName!" /f

if !errorlevel! neq 0 (
    echo Failed to delete the registry key. Please run as administrator or check the profile name.
) else (
    echo Successfully removed the profile from context menu.
)

pause

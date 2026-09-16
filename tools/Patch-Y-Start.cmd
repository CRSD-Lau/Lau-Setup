@echo off
rem Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell
cd /d "%~dp0.."
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0patch-y.ps1"
if errorlevel 1 (
  echo.
  echo Patch-Y stopped with an error. Read the message above before closing.
)
pause

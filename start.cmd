@echo off
cd /d "%~dp0"
set z=observe
set /p z=Zon (observe/dirty/clean) [observe]: 
if not exist "%z%\.claude\settings.json" (echo Okand zon: %z% & pause & exit /b 1)
cd "%z%"
claude

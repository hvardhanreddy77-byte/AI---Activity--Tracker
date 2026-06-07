@echo off
cd /d "C:\Users\hvard\OneDrive\Pictures\Documents\AGENTS"

echo Started at %time% >> startup_debug.txt

"C:\Users\hvard\OneDrive\Pictures\Documents\AGENTS\.venv\Scripts\python.exe" TRACKER1.py

echo Python exited at %time% >> startup_debug.txt

pause
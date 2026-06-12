@echo off
title IELTS Speaking Practice Launcher
echo ===================================================
echo   Starting IELTS Speaking Practice App
echo ===================================================
echo.

:: Check if .env exists
if not exist ".env" (
    echo [WARNING] .env file not found. Creating a template .env file...
    echo GEMINI_API_KEY=> .env
)

:: Start the Python FastAPI backend in a new console window
echo [1/3] Starting FastAPI Backend on Port 8000...
start "IELTS Practice - Backend" cmd /k uvicorn main:app --host 127.0.0.1 --port 8000

:: Start the Vite React frontend in a new console window
echo [2/3] Starting React Frontend on Port 5173...
cd ielts-app
start "IELTS Practice - Frontend" cmd /k npm run dev

:: Wait 2 seconds for servers to initialize
timeout /t 2 /nobreak >nul

:: Launch the default browser
echo [3/3] Opening browser at http://localhost:5173...
start http://localhost:5173

echo.
echo ===================================================
echo   Servers are running! Keep the windows open.
echo   Press any key in this window to close it.
echo ===================================================
pause >nul

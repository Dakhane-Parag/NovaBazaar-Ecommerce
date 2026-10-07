@echo off
REM ============================================
REM Start the frontend development server
REM ============================================

echo Starting frontend...
cd /d frontend
call npm install
call npm run dev

@echo off
REM ============================================
REM Stop all backend services
REM ============================================

echo Stopping all services...
taskkill /FI "WINDOWTITLE eq API Gateway*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq User Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Product Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Search Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Cart Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Inventory Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Order Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Payment Service*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Notification Service*" /F >nul 2>&1
echo All services stopped.

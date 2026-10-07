@echo off
REM ============================================
REM Start all backend services in separate windows
REM ============================================

echo Starting all backend services...

start "API Gateway" cmd /k "cd /d services\api-gateway && pip install -r requirements.txt --quiet && set SERVICE_NAME=api-gateway && set PORT=8100 && python -m uvicorn app.main:app --host 0.0.0.0 --port 8100"

start "User Service" cmd /k "cd /d services\user-service && pip install -r requirements.txt --quiet && set SERVICE_NAME=user-service && set PORT=8101 && python -m uvicorn app.main:app --host 0.0.0.0 --port 8101"

start "Product Service" cmd /k "cd /d services\product-service && pip install -r requirements.txt --quiet && set SERVICE_NAME=product-service && set PORT=8502 && python -m uvicorn app.main:app --host 0.0.0.0 --port 8502"

start "Search Service" cmd /k "cd /d services\search-service && pip install -r requirements.txt --quiet && set SERVICE_NAME=search-service && set PORT=8103 && python -m uvicorn app.main:app --host 0.0.0.0 --port 8103"

start "Cart Service" cmd /k "cd /d services\cart-service && pip install -r requirements.txt --quiet && set SERVICE_NAME=cart-service && set PORT=8104 && python -m uvicorn app.main:app --host 0.0.0.0 --port 8104"

start "Inventory Service" cmd /k "cd /d services\inventory-service && pip install -r requirements.txt --quiet && set SERVICE_NAME=inventory-service && set PORT=8105 && python -m uvicorn app.main:app --host 0.0.0.0 --port 8105"

start "Order Service" cmd /k "cd /d services\order-service && pip install -r requirements.txt --quiet && set SERVICE_NAME=order-service && set PORT=8106 && python -m uvicorn app.main:app --host 0.0.0.0 --port 8106"

start "Payment Service" cmd /k "cd /d services\payment-service && pip install -r requirements.txt --quiet && set SERVICE_NAME=payment-service && set PORT=8107 && python -m uvicorn app.main:app --host 0.0.0.0 --port 8107"

start "Notification Service" cmd /k "cd /d services\notification-service && pip install -r requirements.txt --quiet && set SERVICE_NAME=notification-service && set PORT=8108 && python -m uvicorn app.main:app --host 0.0.0.0 --port 8108"

echo.
echo All services are starting in separate windows.
echo Wait a few seconds for them to initialize.
echo.
echo Verify with: curl http://localhost:8000/health

FROM python:3.12-slim

ARG SERVICE_NAME=unknown-service
ENV SERVICE_NAME=${SERVICE_NAME}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]

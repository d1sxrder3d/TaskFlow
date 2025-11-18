FROM python:3.11-slim

WORKDIR /app

COPY src/rest_api/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "src.rest_api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
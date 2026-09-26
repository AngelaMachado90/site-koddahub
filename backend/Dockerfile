FROM python:3.13.3-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --requirement requirements.txt
COPY backend/app ./app
COPY backend/tests ./tests
RUN groupadd --gid 10001 support && useradd --uid 10001 --gid support --no-create-home support
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]

FROM python:3.9-slim
WORKDIR /app
COPY Django-app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "docker-compose-homework.wsgi:application"]
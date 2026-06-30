FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run static file collection during build (requires fake DB env vars or logic to skip DB checks)
# We will run this dynamically or mock settings
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "python wait_for_db.py && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn backend_project.wsgi:application --bind 0.0.0.0:8000"]

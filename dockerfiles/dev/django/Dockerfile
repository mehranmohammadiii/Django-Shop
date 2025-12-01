FROM python:3.12.11-alpine3.22

# ENV PATH="/opt/venv/bin:$PATH"

LABEL maintainer = "mehranmohammaadiii@gmail.com"
ENV pythonunbuffered=1
RUN apk update && apk add --no-cache postgresql-client libjpeg zlib curl && rm -rf /var/cache/apk/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./core .

# RUN mkdir -p /app/media /app/staticfiles

# RUN python manage.py collectstatic --noinput

# EXPOSE 8000

# CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
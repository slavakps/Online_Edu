FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && \
    apt-get install gcc libpq-dev python3-dev -y --no-install-recommends && \
    apt-get clean
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
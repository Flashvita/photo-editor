# Python Full-stack application with Flet and Django-ninja
### Create .env file and set secret data to frontend and backend
##### touch frontend/.env backend/.env
#### backend/.env:
##### DB_HOST="localhost"
##### CORS_ORIGIN="http://127.0.0.1:8000/"
##### REDIS_HOST="0.0.0.0"
##### REDIS_PORT="6379"
##### DJANGO_SECRET_KEY="django-secret-key"
##### DJANGO_CONFIG="dev"
##### DEFAULT_FROM_EMAIL="DEFAULT_FROM_EMAIL"
##### EMAIL_HOST="EMAIL_HOST"
##### EMAIL_HOST_PASSWORD="EMAIL_HOST_PASSWORD"
##### EMAIL_HOST_USER="EMAIL_HOST_USER"
##### EMAIL_PORT="EMAIL_PORT"
#### frontend/.env:
##### CORS_ORIGIN="http://localhost:8000/"
##### APP_SECRET_KEY="flet-secter-key"

### Run with docker
##### docker-compose build .
##### docker-compose up

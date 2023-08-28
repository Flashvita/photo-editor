# Python Full-stack application with Flet and Django-ninja
#### Create .env file and set secret data to frontend and backend
#### nano backend/.env:
    DB_HOST="localhost"
    CORS_ORIGIN="http://127.0.0.1:8000/"
    REDIS_HOST="redis"
    REDIS_PORT="6379"
    DJANGO_SECRET_KEY="django-secret-key"
    DJANGO_CONFIG="dev"
    DEFAULT_FROM_EMAIL="DEFAULT_FROM_EMAIL"
    EMAIL_HOST="EMAIL_HOST"
    EMAIL_HOST_PASSWORD="EMAIL_HOST_PASSWORD"
    EMAIL_HOST_USER="EMAIL_HOST_USER"
    EMAIL_PORT="EMAIL_PORT"
  
#### nano frontend/.env:
    CORS_ORIGIN="http://localhost:8000/"
    APP_SECRET_KEY="flet-secter-key"

### Run with docker
    docker-compose build .
    docker-compose up -d

### Backend admin - `0.0.0.0:8000/admin/`
### Backend docs - `0.0.0.0:8000/api/docs`
##### Frontend - `0.0.0.0:5000`
##### [Postman collection](https://www.postman.com/planetary-moon-815943/workspace/hummersystem/collection/21235027-053ff9eb-b685-466e-b3ae-28dba6ef29bc?action=share&creator=21235027)

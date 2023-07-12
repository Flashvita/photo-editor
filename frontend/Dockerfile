FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/frontend



COPY ./requirements.txt /app/frontend/requirements.txt
RUN pip install -r requirements.txt
COPY . /app/frontend

#EXPOSE 8080

#CMD ["python", "./main.py"]
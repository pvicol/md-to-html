FROM python:3.12-alpine
EXPOSE 80

WORKDIR /app

COPY public/ /app/

RUN cd /app
CMD ["python3", "-m", "http.server", "80"]

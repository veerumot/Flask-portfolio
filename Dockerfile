FROM python:3.9

RUN apt-get update && \
    pip install Flask && \
    pip install -U flask-cors && \
    pip install pyOpenSSL

RUN mkdir /usr/app \
    && cd /usr/app 

#WORKDIR /usr/app

COPY . /usr/app


# Assuming that main.py is the entry point of your application
CMD ["python3", "/usr/app/main.py"]

EXPOSE 443


FROM ubuntu:latest

LABEL org.opencontainers.image.source https://github.com/gustavocouto/rust-reader-api

ENV TZ=America/Fortaleza

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev tesseract-ocr tesseract-ocr-eng tesseract-ocr-por libsm6 libxext6 libxrender-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev tesseract-ocr tesseract-ocr-eng tesseract-ocr-por

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
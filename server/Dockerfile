FROM python:3.12.1-alpine3.19

WORKDIR /code

EXPOSE 8080

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["python" , "main.py"]
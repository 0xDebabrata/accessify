FROM python:3.11-bookworm

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $PORT

COPY . .

CMD python -m uvicorn main:app --host 0.0.0.0 --port $PORT
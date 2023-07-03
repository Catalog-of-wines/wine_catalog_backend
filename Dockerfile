FROM python:3.10-slim
LABEL maintainer="kaskov.e@gmail.com"

WORKDIR app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install --upgrade pymongo

COPY . /app

# Открытие порта, на котором работает FastAPI
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

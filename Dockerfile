FROM python:3.11-slim
LABEL maintainer="Dmitry Titenkov <lt200711@yandex.ru>"
LABEL version="1.0"
LABEL description="API for miniCRM"
RUN mkdir /app
COPY requirements.txt /app
RUN pip3 install -r  /app/requirements.txt --no-cache-dir -vvv
COPY . /app
WORKDIR /app
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
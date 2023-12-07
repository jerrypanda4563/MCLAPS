FROM python:3.9

WORKDIR /code
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -v -r requirements.txt

COPY ./app /code/app
COPY ./simulations .


EXPOSE 80

CMD ["uvicorn", "app.main:application", "--host", "0.0.0.0", "--port", "80"]
FROM python:3.9

WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -v -r requirements.txt

COPY ./app /code/app
COPY ./tests /code/tests
COPY ./simulations /code/simulations


EXPOSE 80

CMD ["uvicorn", "app.main:application", "--host", "0.0.0.0", "--port", "80"]
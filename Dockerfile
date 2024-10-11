FROM python:3.9

WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -v -r requirements.txt

COPY ./app /code/app
COPY ./tests /code/tests
COPY ./simulations /code/simulations
COPY ./worker.py /code/worker.py

EXPOSE 80

CMD ["sh", "-c", "uvicorn app.main:application --host 0.0.0.0 --port 80 & python worker.py"]




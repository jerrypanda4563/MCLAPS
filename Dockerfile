FROM python:3.9

WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -v -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY ./app /code/app
COPY ./tests /code/tests
COPY ./simulations /code/simulations

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

CMD ["uvicorn", "app.main:application", "--host", "0.0.0.0", "--port", "80"]
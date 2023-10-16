from app.internal import terminal
from fastapi import FastAPI, BackgroundTasks
import uuid

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/simulations/pricing")
async def root(runs: int, age: str, country_of_residence, income_level: str,
               background_tasks: BackgroundTasks):
    
    random_uuid = str(uuid.uuid4())
    # do data validation
    # background_tasks.add_task(terminal.pricing_simulation, runs, age, country_of_residence, income_level)
    # run the simulation async

    # get the output of the simulation to bubble

    # ideally just do data validation, send the request to queue and have a different service process them

    return {"request-id": random_uuid, "status":"pending"}


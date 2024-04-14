from app.internal import runner
from app.internal import data_services
import app.mongo_config as mongo_db
from app.data_models import SimulationParameters
import app.internal.mclapsrl as mclapsrl

from tests import test
from typing import Dict, List

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import os
import json


import uuid



application = FastAPI()

@application.get("/")
async def root():
    return{"API Connection": "Success!"}


@application.get("/connection_test")
async def test_services():
    mclapsrl_client = mclapsrl.mclapsrlClient()
    openai_status=test.openai_connection_test()
    mongo_status=test.mongo_connection_test()
    redis_status=test.redis_connection_test()
    mclapsrl_status = mclapsrl_client.check_service_status()
    return {"OpenAI Status": str(openai_status), "Mongo Status": str(mongo_status), "Redis Status": str(redis_status), "RateLimiter Status": mclapsrl_status}

@application.post("/mclapsrl/new_response")
async def new_response(response_body: dict):
    mclapsrl_client = mclapsrl.mclapsrlClient()
    response = mclapsrl_client.new_response(response_body)
    return {"Response": response}

@application.post("/simulations/new_simulation")
async def new_simulation(sim_param: SimulationParameters,
                                background_tasks: BackgroundTasks):
    
    if test.mongo_connection_test():
        print("MongoDB connection successful.")

        sim_id = str(uuid.uuid4())
        n_of_runs=sim_param.n_of_runs
        n_of_workers=sim_param.workers
        survey_params=sim_param.survey_params
        demographic_params=sim_param.demographic_params
        

        
        data_object: Dict = {
            "_id":sim_id,
            "Survey Name": survey_params.name,
            "Survey Description": survey_params.description,
            "Survey Questions": [json.loads(question.json()) for question in survey_params.questions],
            "Target Demographic": json.loads(demographic_params.json()),
            "Number of Runs": n_of_runs,
            "Completed Runs": 0,
            "Run Status": True,
            "Simulation Result": []
        }
        database = mongo_db.collection_simulations
        database.insert_one(data_object)


        survey_object: Dict[str, List[Dict]] = {
            "description": survey_params.description,
            "questions": [json.loads(question.json()) for question in survey_params.questions]
        }

        demo_object = json.loads(demographic_params.json())

        agent_model = sim_param.agent_params.agent_model
        agent_temperature = sim_param.agent_params.agent_temperature
        


        try:
            background_tasks.add_task(runner.run_simulation, survey_object, demo_object, agent_model, agent_temperature, n_of_runs, sim_id, n_of_workers)
        except Exception as e:
            raise HTTPException(status_code=400,detail=f'Failed to initiate simulation task: {e}.')

        return {"_id": sim_id}
    else:
        raise HTTPException(status_code=500, detail="Error connecting to MongoDB.")



@application.get("/simulations/simulation_status")
async def simulation_status(sim_id: str):
    if test.mongo_connection_test():
        print("MongoDB connection successful.")
        database = mongo_db.collection_simulations
        obj: Dict = database.find_one({"_id": sim_id})
        if obj:
            run_status = obj["Run Status"]
            completed_runs = obj["Completed Runs"]
            total_runs = obj["Number of Runs"]
            return {"Run Status": run_status, "Completion Percentage": f"{completed_runs} out of {total_runs} runs completed."}
        else:
            raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")
    else:
        raise HTTPException(status_code=500, detail="Error connecting to MongoDB.")
        
    
    

@application.get("/simulations/load_simulation")
async def load_simulation(sim_id: str) -> Dict:
    if test.mongo_connection_test():
        database = mongo_db.collection_simulations
        obj: Dict = database.find_one({"_id": sim_id})
        if obj:
            return obj
        else:
            raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")
    else:
        raise HTTPException(status_code=500, detail="Error connecting to MongoDB.")
        
        
@application.get("/simulations/load_simulation/csv")
async def load_simulation_csv(sim_id: str, file_path = "./simulations"):
    if test.mongo_connection_test():
        print("MongoDB connection successful.")
        database = mongo_db.collection_simulations
        obj: Dict = database.find_one({"_id": sim_id})
        if obj:    
            try:
                data_services.create_csv_from_simulation_results(sim_data=obj)
                file_path = f"{file_path}/{sim_id}_Simulation_Results.csv"
                survey_name: str = obj["Survey Name"]

            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error creating CSV file: {e}")
            if not os.path.isfile(file_path):
                raise HTTPException(status_code=404, detail="CSV file not found.")
            
            return FileResponse(path=file_path, media_type='text/csv', filename=f"{survey_name}_{sim_id}_Simulation_Results.csv")
        
        else:
            raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")
    else:
        raise HTTPException(status_code=500, detail="Error connecting to MongoDB.")
       



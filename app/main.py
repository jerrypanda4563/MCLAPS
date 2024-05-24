from app.internal import runner
from app.internal import data_services
import app.mongo_config as mongo_db
from app.data_models import SimulationParameters
import app.api_clients.mclapsrl as mclapsrl

from tests import test
from typing import Dict, List

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import os
import json


import uuid

from app.api_clients.mclaps_demgen import MclapsDemgenClient





demgen_client = MclapsDemgenClient()
application = FastAPI()




@application.get("/")
async def root():
    return{"API Connection": "Success!"}


@application.get("/connection_test")
async def test_services():

    openai_status=test.openai_connection_test()
    mongo_status=test.mongo_connection_test()
    redis_status=test.redis_connection_test()
    mclapsrl_client = mclapsrl.mclapsrlClient()
    mclapsrl_status = mclapsrl_client.check_service_status()
    demgen_client = MclapsDemgenClient()
    demgen_status = demgen_client.service_status()

    return {
        "OpenAI Status": openai_status, 
        "Mongo Status": mongo_status,
        "Redis Status": redis_status, 
        "RateLimiter Status": mclapsrl_status, 
        "Demgen Status": demgen_status
        }




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


        agent_model = sim_param.agent_params.agent_model
        agent_temperature = sim_param.agent_params.agent_temperature
        


        try:
            background_tasks.add_task(runner.run_simulation, survey_object, demographic_params, agent_model, agent_temperature, n_of_runs, sim_id, n_of_workers)
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
       

#temporary import 
# import openai
# import app.settings as settings
# from app.data_models import open_ai_models

# openai.api_key = settings.OPEN_AI_KEY


#temporary endpoint
# @application.get("/mclapsrl/test")
# async def response_test():
#     mclapsrl_client = mclapsrl.mclapsrlClient()
#     completion = openai.ChatCompletion.create(
#                     model = "gpt-4-turbo",
#                     messages=[
#                             {"role": "system", "content": "helpful assistant"},
#                             {"role": "user", "content": "who won the world series in 1995"},
#                         ],
#                     temperature=0.7,
#                     max_tokens=512,
#                     n=1  
#                     )
#     print(completion.model)
#     try:
#         loggin_result = mclapsrl_client.new_response(completion)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f'Failed to log response: {e}.')
#     return {"Response": loggin_result}

# @application.get("/mclapsrl/model_status")
# async def model_status_test(model: open_ai_models):
#     mclapsrl_client = mclapsrl.mclapsrlClient()
#     model_status = mclapsrl_client.get_counter_status(model)
#     return model_status

# @application.get("/mclapsrl/create_counter")
# async def create_counter_test(model: open_ai_models):
#     try:
#         mclapsrl_client = mclapsrl.mclapsrlClient()
#         counter_status = mclapsrl_client.create_counter(model)
#         return {"Counter Status": counter_status}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f'Failed to create counter: {e}.')

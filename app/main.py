from app.internal import simulation_runner as runner
from app.internal import data_services, demgen
import app.redis_config as redis_config
import app.mongo_config as mongo_config
from app.redis_config import cache
import app.mongo_config as mongo_db
from tests import test

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import os
import sys
from pydantic import BaseModel, Field, validator


from typing import List, Dict, Type, Optional, Union
import uuid
import json



application = FastAPI()

#Demographic validation model
class DemographicModel(BaseModel):
    sex_at_birth: Optional[str] = None
    gender_identity: Optional[str] = None
    age: Optional[str] = None
    marital_status: Optional[str] = None
    sexual_orientation: Optional[str] = None
    nationality: Optional[str] = None
    country_of_residence: Optional[str] = None
    state_province: Optional[str] = None
    city: Optional[str] = None
    rural_or_urban: Optional[str] = None
    type_of_residence: Optional[str] = None
    length_of_residence: Optional[str] = None
    level_of_education: Optional[str] = None
    student_status: Optional[str] = None
    field_of_study: Optional[str] = None
    occupational_area: Optional[str] = None
    annual_income_level: Optional[str] = None
    employment_status: Optional[str] = None
    home_ownership: Optional[str] = None
    ethnicity: Optional[str] = None
    languages_spoken: Optional[str] = None
    religion: Optional[str] = None
    cultural_practices: Optional[str] = None
    immigration_status: Optional[str] = None
    hobbies_and_interests: Optional[str] = None
    shopping_motivations: Optional[str] = None
    shopping_habits: Optional[str] = None
    shopping_channels: Optional[str] = None
    shopping_frequency: Optional[str] = None
    dietary_preferences: Optional[str] = None
    physical_activity_levels: Optional[str] = None
    social_media_usage: Optional[str] = None
    travel_habits: Optional[str] = None
    alcohol_use: Optional[str] = None
    tobacco_and_vape_use: Optional[str] = None
    technology_usage: Optional[str] = None
    family_structure: Optional[str] = None
    household_size: Optional[str] = None
    number_of_children: Optional[str] = None
    pet_ownership: Optional[str] = None
    number_of_pets: Optional[str] = None
    relationship_status: Optional[str] = None
    caregiving_responsibilities: Optional[str] = None
    general_health_status: Optional[str] = None
    disabilities_or_chronic_illnesses: Optional[str] = None
    mental_health_status: Optional[str] = None
    health_insurance_status: Optional[str] = None
    access_to_healthcare: Optional[str] = None
    political_affiliation: Optional[str] = None
    voting_behavior: Optional[str] = None
    political_engagement: Optional[str] = None

    class Config:
        extra = "forbid"  # Forbids any extra fields not defined in the model

#survey validation model
class ShortAnswerQuestion(BaseModel):
    type: str = Field("short answer", Literal=True)
    question: str
    answer: Optional[str] = None

class LongAnswerQuestion(BaseModel):
    type: str = Field("long answer", Literal=True)
    question: str
    answer: Optional[str] = None

class MultipleChoiceQuestion(BaseModel):
    type: str = Field("multiple choice", Literal=True)
    question: str
    choices: List[str]
    answer: Optional[str] = None

class CheckboxesQuestion(BaseModel):
    type: str = Field("checkboxes", Literal=True)
    question: str
    choices: List[str]
    answer: Optional[List[str]] = None

class LinearScaleQuestion(BaseModel):
    type: str = Field("linear scale", Literal=True)
    question: str
    min_value: int
    max_value: int
    answer: Optional[int] = None

class SurveyModel(BaseModel):
    name: str
    description: Optional[str] = None
    questions: List[Union[ShortAnswerQuestion, LongAnswerQuestion, MultipleChoiceQuestion, CheckboxesQuestion, LinearScaleQuestion]]

    @validator('questions', each_item=True)
    def check_question_type(cls, v):
        if v.type not in ["short answer", "long answer", "multiple choice", "checkboxes", "linear scale"]:
            raise ValueError('Invalid question type')
        return v

class SimulationParameters(BaseModel):
    demographic_params: DemographicModel
    survey_params: SurveyModel
    n_of_runs: int
    class Config:
        extra="forbid"
###

##core functions
def check_existence(sim_id: str) -> bool:
    try:
        cache_existence=cache.exists(sim_id)
        if cache_existence:
            return True
        
        db_existence=mongo_db.collection_simulations.find_one({"_id": sim_id})
        if db_existence:
            return True
    except redis_config.redis.RedisError as e:
        print(f"Redis error: {e}")
    except mongo_config.PyMongoError as e:
        print(f"MongoDB error: {e}")
        
        return False


    raise HTTPException(status_code=500, detail="Error checking survey status.") 

def check_completion(sim_id: str) -> bool:
    if check_existence(sim_id) is True:
        
        try:
            cache_completion=cache.hget(sim_id, "Simulation Status")
            if cache_completion.decode('utf-8').lower() == 'true':
                return True
            db_completion=mongo_db.collection_simulations.find_one({"_id": sim_id})
            if db_completion and db_completion.get("Simulation Status", "").lower() == 'true':
                return True
            return False
        except redis_config.redis.RedisError as e:
            print(f"Redis error: {e}")
        except mongo_config.PyMongoError as e:
                print(f"MongoDB error: {e}") 
        except Exception:
            try: 
                db_completion=mongo_db.collection_simulations.find_one({"_id": sim_id})
                if db_completion and db_completion.get("Simulation Status", "").lower() == 'true':
                    return True
                return False
            except mongo_config.PyMongoError as e:
                print(f"MongoDB error: {e}")
            
        
        
        raise HTTPException(status_code=500, detail="Error checking survey status.") 
    
    else:
        raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")


def mongo_load_simulation(sim_id:str) -> bool:
    try:
        if check_existence(sim_id) is False:
            raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")
        
        mongo_data = mongo_db.collection_simulations.find_one({"_id": sim_id})
        # Iterate over the fields and store them in Redis
        for key, value in mongo_data.items():
            if key in ["Survey Questions", "Target Demographic", "Simulation Result"]:
                # Serialize lists and dicts as JSON
                cache.hset(sim_id, key, json.dumps(value))
            else:
                # Store other data types as strings
                cache.hset(sim_id, key, str(value))

        print(f"Data loaded into Redis for sim_id: {sim_id}")
        return True

    except Exception as e:
        print(f"Error loading data from MongoDB to Redis: {e}")
        return False

    

@application.get("/")
async def root():
    return{"API Connection": "Success!"}


@application.get("/connection_test")
async def test_services():
    openai_status=test.openai_connection_test()
    mongo_status=test.mongo_connection_test()
    redis_status=test.redis_connection_test()
    return {"OpenAI Status": str(openai_status), "Mongo Status": str(mongo_status), "Redis Status": str(redis_status)}



@application.post("/simulations/new_simulation")
async def new_simulation(sim_param: SimulationParameters,
                                background_tasks: BackgroundTasks):
    
    sim_id = str(uuid.uuid4())
    n_of_runs=sim_param.n_of_runs
    survey_params=sim_param.survey_params
    demographic_params=sim_param.demographic_params
    
    try:
        cache.hset(sim_id, "Survey Name", survey_params.name)
        cache.hset(sim_id, "Survey Description", survey_params.description)
        cache.hset(sim_id, "Survey Questions", json.dumps([question.json() for question in survey_params.questions]))
        cache.hset(sim_id, "Target Demographic", json.dumps(demographic_params.json()))
        cache.hset(sim_id, "Number of Runs", n_of_runs)
        cache.hset(sim_id, "Simulation Status", "false" )
    except Exception as e:
        print({e})
        raise HTTPException(status_code=400, detail=f"Failed to create simulation object: {e}")
    
    demo_data=demographic_params.json()
    survey_data={
        "Survey Name": survey_params.name,
        "Survey Description": survey_params.description,
        "Survey Questions": [question.json() for question in survey_params.questions]
    }

    try:
        background_tasks.add_task(runner.get_simulation_data, n_of_runs, survey_data, demo_data, sim_id)
    except Exception as e:
        raise HTTPException(status_code=400,detail=f'Failed to initiate simulation task: {e}.')

    return {"_id": sim_id, "Simulation Status": "In progress"}



@application.get("/simulations/simulation_status")
async def simulation_status(sim_id: str):
    
    if check_existence(sim_id) is False:
        raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")
    
    if check_completion(sim_id) is False:
        # mongo_load_simulation(sim_id)
        n_total=int(cache.hget(sim_id, "Number of Runs").decode("utf-8"))
        n_completed=len(cache.lrange('r'+sim_id,0,-1))
        simulation_percentage= (n_completed/n_total)*100
        return {"Simulation Status": str(simulation_percentage)+"%"}
    
    else:
        return {"Simulation Status": "Complete"}
    
    

@application.get("/simulations/load_simulation")
async def load_simulation(sim_id: str):
    
    if check_existence(sim_id) is False:
        raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")
    
    if check_completion(sim_id) is True:
        try:
            #trying to load from cache
            cached_data=cache.hgetall(sim_id)
            if cached_data:
                data={
                    "_id":sim_id,
                    "Survey Name":(cache.hget(sim_id,"Survey Name")).decode('utf-8'),
                    "Survey Description":cache.hget(sim_id, "Survey Description").decode('utf-8'),
                    "Survey Questions": json.loads(cache.hget(sim_id, "Survey Questions").decode('utf-8')),
                    "Target Demographic": json.loads(cache.hget(sim_id, "Target Demographic").decode('utf-8')),
                    "Number of Runs": cache.hget(sim_id, "Number of Runs").decode('utf-8'),
                    "Simulation Status": cache.hget(sim_id, "Simulation Status").decode('utf-8'),
                    "Simulation Result": json.loads(cache.hget(sim_id,"Simulation Result").decode('utf-8'))
                }
                print(f'Data returned from cache')
                return data
            
            #trying to load from mongodb
            query=mongo_db.collection_simulations.find_one({"_id":sim_id})
            if query:
                print(f'Data returned from MongoDB')
                return query
        
        except Exception as e:
                print(f"Error occurred: {e}")
                raise HTTPException(status_code=400, detail=f"Failed to load file, please try again later.")
    
    else:
        try:
            n_total=int(cache.hget(sim_id, "Number of Runs").decode("utf-8"))
            n_completed=len(cache.lrange('r'+sim_id,0,-1))
            simulation_percentage= (n_completed/n_total)*100
            return{"detail": "Simulation in progress:"+str(simulation_percentage)+"%"}
        except Exception as e:
            raise HTTPException(status_code=400, detail= f'Simulation request does not exist: {e}')
        
        
@application.get("/simulations/load_simulation/csv")
async def load_simulation_csv(sim_id: str, file_path = "./simulations"):
    ## check if simulation complete first
    if check_existence(sim_id) is False:
        raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")

    if check_completion(sim_id) is True:
        try:
            
            data_services.create_csv_from_simulation_results(sim_id)
            file_path = f"{file_path}/{sim_id}_Simulation_Results.csv"

            if not os.path.isfile(file_path):
                raise HTTPException(status_code=404, detail="CSV file not found.")
            return FileResponse(path=file_path, media_type='text/csv', filename=f"{sim_id}_Simulation_Results.csv")
        
        ### NEW try exception block for loading from redis
        except Exception as e: 
            print(f'Cache not available {e}, trying to load from Mongo.')
            try:
                mongo_load_simulation(sim_id)
                data_services.create_csv_from_simulation_results(sim_id)
                file_path = f"{file_path}/{sim_id}_Simulation_Results.csv"
                if not os.path.isfile(file_path):
                    raise HTTPException(status_code=404, detail="CSV file not found.")
                return FileResponse(path=file_path, media_type='text/csv', filename=f"{sim_id}_Simulation_Results.csv")
           
            except Exception as e:
                print(f'error loading csv {e}')
                raise HTTPException(status_code=500, detail = f'Error loading csv: {e}')
    
    else: 
        try:
            n_total=int(cache.hget(sim_id, "Number of Runs").decode("utf-8"))
            n_completed=len(cache.lrange('r'+sim_id,0,-1))
            simulation_percentage= (n_completed/n_total)*100
            return{"detail": "Simulation in progress:"+str(simulation_percentage)+"%"}
        except Exception as e:
            raise HTTPException(status_code=400, detail= f'{e}')








##### REDUNDANT CODE #####
#start-up event
# @application.on_event("startup")
# async def tests():
#     print("Running startup connection tests...")
#     openai_status=test.openai_connection_test()
#     if openai_status is False:
#         print("OpenAI connection failed")
#         sys.exit(1)
#     mongo_status=test.mongo_connection_test()
#     if mongo_status is False:
#         print("MongoDB connection failed")
#         sys.exit(1)
#     redis_status=test.redis_connection_test()
#     if redis_status is False:
#         print("Redis connection failed")
#         sys.exit(1)


#endpoints
# @application.post("/demgen_lite")
# async def demgen_lite(prompt: str):
#     demographic = json.loads(demgen.nerfed_generate_demographic(prompt))
#     return demographic


# @application.post("/survey/create_survey")
# async def create_survey(survey_model: SurveyModel, demographic_model: DemographicModel):
#     sim_id = str(uuid.uuid4()) 
#     survey_questions = [question.json() for question in survey_model.questions]
#     try:
#         cache.hset(sim_id, "Survey Name", survey_model.name)
#         cache.hset(sim_id, "Survey Description", survey_model.description)
#         cache.hset(sim_id, "Survey Questions", json.dumps(survey_questions))
#         cache.hset(sim_id, "Target Demographic", json.dumps(demographic_model.json()))
#     except Exception as e:
#         print({e})
#         raise HTTPException(status_code=400, detail=f"Failed to create survey: {e}")
    
#     data={
#         "_id":sim_id,
#         "Survey Name":(cache.hget(sim_id,"Survey Name")).decode('utf-8'),
#         "Survey Description":cache.hget(sim_id, "Survey Description").decode('utf-8'),
#         "Survey Questions": json.loads(cache.hget(sim_id, "Survey Questions").decode('utf-8')),
#         "Target Demographic": json.loads(cache.hget(sim_id, "Target Demographic").decode('utf-8'))
#     }
#     return data ### json for creating new Simulation File in Bubble


# @application.post("/simulations/new_simulation")   
# async def new_simulation(sim_param: SimulationParameters,
#                                 background_tasks: BackgroundTasks):
    
#     sim_id=sim_param.sim_id
#     n_of_runs=sim_param.n_of_runs
#     if check_existence is False:
#         raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")
    
#     #loads in demo data from cache and creates an instance of the ClassDemographic
#     if check_completion is True:
#         return {"detail": "Simulation {sim_id} is completed."}
    
#     demo_data=json.loads(json.loads(cache.hget(sim_id, "Target Demographic").decode('utf-8')))
#     survey_data={
#         "Survey Name": cache.hget(sim_id, "Survey Name").decode('utf-8'),
#         "Survey Description": cache.hget(sim_id, "Survey Description").decode('utf-8'),
#         "Survey Questions": json.loads(cache.hget(sim_id, "Survey Questions").decode('utf-8'))
#     }
    
#     #initialize simulation
#     cache.hset(sim_id, "Number of Runs", n_of_runs)
#     cache.hset(sim_id, "Simulation Status", "false" )
#     try:
#         background_tasks.add_task(runner.get_simulation_data, n_of_runs, survey_data, demo_data, sim_id)
#     except Exception as e:
#         raise HTTPException(status_code=400,detail=f'Failed to initiate simulation task: {e}.')

#     return {"_id": sim_id, "Simulation Status": "In progress"} ##sth indicatiing simulation status of a file to client status



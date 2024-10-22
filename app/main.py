import rq.registry
from app.internal import runner
from app.internal import data_services
import app.mongo_config as mongo_db
from app.redis_config import cache 
from app.data_models import SimulationParameters, OpenAIModels
import app.api_clients.mclapsrl as mclapsrl
from app.api_clients.mclaps_demgen import MclapsDemgenClient, DemgenRequest
from tests import test
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from rq.registry import FinishedJobRegistry, StartedJobRegistry, FailedJobRegistry
import json

import rq


import uuid

from app.api_clients.mclaps_demgen import MclapsDemgenClient

import logging
import traceback




demgen_client = MclapsDemgenClient()
application = FastAPI()
queue = rq.Queue(name = 'sim_requests', connection = cache, default_timeout=7200)
openai_models = OpenAIModels()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



@application.get("/")
async def root():
    return{"API Connection": "Success!"}

from app.data_models import DemographicModel
@application.get("/demgen_test")
async def demgen_test():
    endpoint_status = []

    try: 
        demgen_client.read_root()
        endpoint_status.append({"read_root": True})
    except Exception as e:
        traceback.print_exc()
        print(f"Root Error: {e}")
        endpoint_status.append({"read_root": False})

    try:
        demgen_client.array_status()
        endpoint_status.append({"array_status": True})
    except Exception as e:
        traceback.print_exc()
        print (f"Array Error: {e}")
        endpoint_status.append({"array_status": False})


    try:
        response = demgen_client.demgen_request(DemgenRequest(number_of_samples=1, batch_size=250, sim_id = str(uuid.uuid4()), sampling_conditions = DemographicModel()))
        endpoint_status.append({"demgen_request": True})
    except Exception as e:
        traceback.print_exc()
        print(f"Demgen Request Error: {e}")
        endpoint_status.append({"demgen_request": False})
    
    try: 
        demgen_client.get_task_status(response["task_ids"][0])
        endpoint_status.append({"get_task_status": True})   
    except Exception as e:
        traceback.print_exc()
        print(f"Get Task Status Error: {e}")
        endpoint_status.append({"get_task_status": False})

    try:
        demgen_client.get_task_results(response["task_ids"][0])        
        endpoint_status.append({"get_task_results": True})
    except Exception as e:
        traceback.print_exc()
        print(f"Get Task Results Error: {e}")
        endpoint_status.append({"get_task_results": False})

    try:
        demgen_client.get_dataset(response["dataset_id"])
        endpoint_status.append({"get_dataset": True})
    except Exception as e:
        traceback.print_exc()
        print(f"Get Dataset Error: {e}")
        endpoint_status.append({"get_dataset": False})
    
    return endpoint_status

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


           


@application.get("/simulations/all_tasks")
async def all_tasks():
    try:
        queued_jobs = queue.jobs
        queued_job_ids = [job.id for job in queued_jobs]

        # Get started jobs
        started_registry = StartedJobRegistry(queue=queue)
        started_job_ids = started_registry.get_job_ids()


        # Get finished jobs
        finished_registry = FinishedJobRegistry(queue=queue)
        finished_job_ids = finished_registry.get_job_ids()


        # Get failed jobs
        failed_registry = FailedJobRegistry(queue=queue)
        failed_job_ids = failed_registry.get_job_ids()

        return {"finished tasks":  finished_job_ids, "started tasks": started_job_ids,  "queued tasks": queued_job_ids, "failed tasks": failed_job_ids}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {e}")

from rq.job import Job
@application.get("/simulations/kill_all")
async def kill_all():
    try:
        # Retrieve all job IDs in the queue (queued jobs)
        job_ids = queue.job_ids
        
        # Cancel jobs in the queue
        for job_id in job_ids:
            job = Job.fetch(job_id, connection=queue.connection)
            job.cancel()  # Cancel the queued job

        # Get the registry of started jobs
        registry = StartedJobRegistry(queue=queue)
        started_job_ids = registry.get_job_ids()

        # Cancel jobs that are currently started
        for job_id in started_job_ids:
            job = Job.fetch(job_id, connection=queue.connection)
            if job.is_started:  # Check if the job is started
                job.cancel()  # Cancel the started job

        # Optionally: You could also empty the queue after canceling all jobs
        queue.empty()
        demgen_client = MclapsDemgenClient()
        demgen_client.kill_all_task()

        return {"message": "All queued and started tasks killed in main simulation and agent generation."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing tasks: {e}")

@application.get("/simulations/clear_queue")
async def clear_queue():
    try:
        queue.empty()
        return {"message": "Queue cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing tasks: {e}")


@application.post("/simulations/new_simulation")
async def new_simulation(sim_param: SimulationParameters):
    
    if openai_models.check_model(sim_param.agent_params.agent_model) == False:
        raise HTTPException(status_code=400, detail=f"Model {sim_param.agent_params.agent_model} invalid, available models: {openai_models.list_models()}")
    if openai_models.check_model(sim_param.agent_params.embedding_model) == False:
        raise HTTPException(status_code=400, detail=f"Model {sim_param.agent_params.embedding_model} invalid, available models: {openai_models.list_models()}")

    if test.mongo_connection_test():
        print("database connection successful.")
    else:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error connecting to database.")
    

    simulation_batch_size = sim_param.batch_size
    sim_id = str(uuid.uuid4())
    n_of_runs=sim_param.n_of_runs
    n_of_workers=sim_param.workers
    survey_params=sim_param.survey_params
    demographic_params=sim_param.demographic_params
    agent_params=sim_param.agent_params
    survey_object: dict = survey_params.dict()
    

    #############send demgen request here
    demgen = MclapsDemgenClient()
    try:
        demgen_task = demgen.demgen_request(DemgenRequest(number_of_samples=n_of_runs, batch_size=simulation_batch_size, sim_id = sim_id, sampling_conditions = demographic_params))
        print(f"Demgen request successful: {demgen_task}")
    except Exception as e:
        print(f"Demgen request failed: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500,detail=f'Failed to initiate demographic generation task: {e}.')
    
    demgen_task_ids = demgen_task["task_ids"] #list of task ids for each batch
    print(f"Demgen task ids: {demgen_task_ids}")
    
    #batching the simulation runs
    batch_size = simulation_batch_size
    if n_of_runs > batch_size:
    
        n_of_batches = n_of_runs // batch_size
        remainder_batch_size = n_of_runs % batch_size
        request_batch_sizes = [i for i in [batch_size] * n_of_batches + [remainder_batch_size] if i != 0]
        request_batches = []
        for batch, demgen_task_id in zip(request_batch_sizes, demgen_task_ids):
            request_batch = (batch, demgen_task_id)
            request_batches.append(request_batch)
    else:
        request_batches = [(n_of_runs, demgen_task_ids[0])]


    try:
        tasks: list[Job] = []
        for request_batch in request_batches:
            task = queue.enqueue(
                runner.run_simulation, 
                args = (sim_id, request_batch[1], survey_object, agent_params, n_of_workers), 
                retry = rq.Retry(max=3, interval = 10), 
                results_ttl = 7200, 
                timeout = 7200)
            tasks.append(task)
            
        print(f"runner tasks initiated: {tasks}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400,detail=f'Failed to initiate simulation task: {e}.') 
    
    try:
        request_batch_states: dict = {demgen_task_id: True for demgen_task_id in demgen_task_ids}
        total_timesteps: int = n_of_runs * len(survey_object["questions"])
        data_object: Dict = {
            "_id":sim_id,
            "batch_states": request_batch_states,
            "name": survey_params.name,
            "context": survey_params.context,
            "iterations": [json.loads(question.json()) for question in survey_params.questions],
            "demographic_sampling_conditions": json.loads(demographic_params.json()),
            "n_of_runs": n_of_runs,
            "completed_runs": 0,
            "total_timesteps": total_timesteps,
            "completed_timesteps": 0,
            "run_status": True,
            "progress": 0,
            "result_ids": []
        }
        database = mongo_db.database["requests"]
        database.insert_one(data_object)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400,detail=f'Failed to create simulation object in data: {e}.')

    try:
        queued_jobs = queue.get_job_ids()
        # Fetch started jobs, get queue positions of tasks
        started_registry = rq.registry.StartedJobRegistry(queue=queue)
        started_job_ids = started_registry.get_job_ids()
        all_job_ids = queued_jobs + started_job_ids
        job_position_map = {job_id: idx + 1 for idx, job_id in enumerate(all_job_ids)}
        queue_positions = [job_position_map.get(task.id, -1) for task in tasks]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400,detail=f'Failed to get job queue positions: {e}.')
    
    return {"task_id": [task.id for task in tasks], "simulation_id": sim_id, "queue_position": queue_positions} 
        






##works
@application.get("/simulations/status")
def sim_status(sim_id: str) -> Dict:
    if test.mongo_connection_test():
        database = mongo_db.database["requests"]
        request_object_query = {"_id": sim_id}
        batch_states:dict = database.find_one(request_object_query)["batch_states"]
        progress = 100 * (database.find_one(request_object_query)["completed_timesteps"]/database.find_one(request_object_query)["total_timesteps"])
        if all(batch_states.values()) == False:
            run_status = False
            database.update_one(request_object_query, {"$set":{"run_status": run_status}})
            database.update_one(request_object_query, {"$set":{"progress": progress}})
        else:
            run_status = True
            database.update_one(request_object_query, {"$set":{"progress": progress}})
        
        return {"sim_id": sim_id, "run_status": run_status, "progress": f"{progress}%"}
    
    else:
        raise HTTPException(status_code=404, detail=f"Simulation with ID {sim_id} doesn't exist, please create simulation first.")




## result obj and req obj schema ref
# {
#             "_id":sim_id,
#             "batch_states": request_batch_states,
#             "name": survey_params.name,
#             "context": survey_params.context,
#             "iterations": [json.loads(question.json()) for question in survey_params.questions],
#             "demographic_sampling_conditions": json.loads(demographic_params.json()),
#             "n_of_runs": n_of_runs,
#             "completed_runs": 0,
#             "total_timesteps": total_timesteps,
#             "completed_timesteps": 0,
#             "run_status": True,
#             "progress": 0,
#             "result_ids": []
#         }

@application.get("/simulations/load_simulation")
async def load_simulation(sim_id: str, csv: Optional[bool] = True):
    simulation_json = data_services.load_simulation_json(sim_id)
    if csv:
        file_path = "./simulations"
        file = data_services.load_simulation_csv(sim_id, file_path)
        return FileResponse(file)
    else:
        return simulation_json
        
  






       



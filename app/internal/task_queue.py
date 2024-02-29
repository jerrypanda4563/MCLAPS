from fastapi import BackgroundTasks
import runner
from typing import Dict, Optional, List
from concurrent.futures import ProcessPoolExecutor, as_completed

class RunnerTaskQueue:
    def __init__(self):
        self.queue: List[tuple] = []
        self.running = 0

    def run_next_task(self):
       
        survey, demographic_parameters, n_of_runs, sim_id, n_workers = self.queue.pop(0)
            
        


    def add_task(self, survey: Dict, demographic_parameters: Dict, n_of_runs: int, sim_id: str, n_workers: Optional[int]=5):
        self.queue.append((survey, demographic_parameters, n_of_runs, sim_id, n_workers))
        if self.running < 3:
            self.run_next_task()
        

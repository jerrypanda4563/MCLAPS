from app.internal import response_agent 
from app.data_models import SurveyModel, DemographicModel, AgentParameters
import traceback
from typing import Dict, List, Optional
from app.internal.prompt_payloads import input_question, initialization_prompt

import json
import openai.error
import time



##world state, should essentially be one fat as fuck graph database initialized togther with a set of self persistent (or not) agents

class WorldState:

    def __init__(self, list_of_agents: 
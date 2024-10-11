from app import settings
import openai
from openai.error import OpenAIError, Timeout, ServiceUnavailableError, RateLimitError, APIError
from typing import Optional, Literal
from app.api_clients import mclapsrl
import numpy as np
import time
import traceback
import warnings


rate_limiter = mclapsrl.mclapsrlClient()
openai.api_key = settings.OPEN_AI_KEY


def model_response(query_message: str, assistant_message: str, system_message: str , model_name: str, json_mode: bool, temperature: float, response_length: int ) -> str:
    
    
    #json mode
    if json_mode == True:
        response_type = {"type": "json_object"}
    else:
        response_type = {"type": "text"}
    
    retries = 3

    while retries > 0:
        while rate_limiter.model_status(model_name) == False:
            time.sleep(10)
            continue
        try:
            completion = openai.ChatCompletion.create(
                    model = model_name,
                    response_format = response_type,
                    messages=[
                            {"role": "system", "content": system_message},
                            {"role": "assistant", "content": assistant_message},
                            {"role": "user", "content": query_message},
                        ],
                    temperature = temperature,
                    max_tokens = response_length,
                    n=1  
                    )
            rate_limiter.new_response(completion)
            response = completion.choices[0].message.content
            return response
        except (OpenAIError, Timeout, ServiceUnavailableError, APIError) as e:
            warnings.warn(f"server returned an error while processing query: {query_message}. {e}")
            traceback.print_exc()
            rate_limiter.model_break(model_name, 10)
            retries -= 1
            continue
        except RateLimitError as e:
            warnings.warn(f"rate limit exceeded while processing query: {query_message}. {e}")
            traceback.print_exc()
            rate_limiter.model_break(model_name, 60)
            retries -= 1
            continue
        except Exception as e:
            warnings.warn(f"an exception occurred while processing query: {query_message}. {e}")
            traceback.print_exc()
            rate_limiter.model_break(model_name, 10)
            retries -= 1
            continue
            
    else:
        warnings.warn(f"a default response was returned for model query: {query_message}")
        default_response = "\n".join([system_message, assistant_message, query_message])
        return default_response
    



##module for contextualizing visual data for memory and retrieval

import json
import base64
from pydantic import BaseModel, constr
from typing import List, Dict, Optional
import openai
from app import settings
from


openai.api_key = settings.OPEN_AI_KEY

image_directory = "./app/internal/image_temp"



def encode_image(image_id: str ) -> base64 :
    image_path = f"{image_directory}/{image_id}.jpg"
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')



#creates natural language image understanding based on image data and memory data
def image_comprehension(base64_image) -> str: 
    response = openai.ChatCompletion.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": "You are a computer."},
            {"role": "user", "content": f"Describe the image: {base64_image}"}
        ]

    )



import app.internal.response_agent as response_agent
import app.internal.demgen as demgen
import json


demographic_data =demgen.generate_demographic( 
    {
      "sex_at_birth": None,
      "gender_identity": None,
      "age": "22 to 29",
      "marital_status": None,
      "sexual_orientation": None,
      "nationality": None,
      "country_of_residence": "United Kingdom",
      "state_province": None,
      "city": None,
      "rural_or_urban": None,
      "type_of_residence": None,
      "length_of_residence": None,
      "level_of_education": "Bachelor, Master",
      "student_status": None,
      "field_of_study": None,
      "occupational_area": None,
      "annual_income_level": "30000£ to 45000£",
      "employment_status": None,
      "home_ownership": None,
      "ethnicity": None,
      "languages_spoken": None,
      "religion": None,
      "cultural_practices": None,
      "immigration_status": None,
      "hobbies_and_interests": None,
      "shopping_motivations": None,
      "shopping_habits": None,
      "shopping_channels": "Primary online",
      "shopping_frequency": None,
      "dietary_preferences": None,
      "physical_activity_levels": None,
      "social_media_usage": None,
      "travel_habits": None,
      "alcohol_use": None,
      "tobacco_and_vape_use": None,
      "technology_usage": None,
      "family_structure": None,
      "household_size": None,
      "number_of_children": None,
      "pet_ownership": None,
      "number_of_pets": None,
      "relationship_status": None,
      "caregiving_responsibilities": None,
      "general_health_status": None,
      "disabilities_or_chronic_illnesses": None,
      "mental_health_status": None,
      "health_insurance_status": None,
      "access_to_healthcare": None,
      "political_affiliation": None,
      "voting_behavior": None,
      "political_engagement": None
    }
    )

demo_data = json.loads(demographic_data)


agent = response_agent.Agent(instruction="You are behaving like a real person.", model = "gpt-3.5-turbo-0125", json_mode = True)
survey_context = "The product is a smartphone with the following features: \nDisplay: Vertically foldable 6.2-inch Dynamic AMOLED with high refresh rate, secondary 1.5 inch AMOLED display\nProcessor:Snapdragon Gen 3 \nCamera: Triple-camera setup with a 64MP main sensor \nBattery: 4,500mAh with fast charging \nConnectivity: 5G, Wi-Fi 6 \nStorage: 256GB/512GB expandable \nRAM: 8/12GB \nOther: Aluminium frame and gorilla glass front and back, IP68 water resistance"
agent.inject_memory(survey_context)
for k, v in demo_data.items():
    agent.inject_memory(f"{k}: {v}")


survey_questions = [{
          "type": "short answer",
          "question": "At what price in GBP would you consider the product to be so expensive that you would not consider buying it?",
          "answer": "int"
        },
        {
            "type": "short answer",
            "question": "At what price in GBP would you consider the product to be priced so low that you would feel the quality couldn’t be very good?",
            "answer": "int"
          },
          {
            "type": "short answer",
            "question": "At what price in GBP would you consider the product starting to get expensive, so that it is not out of the question, but you would have to give some thought to buying it?",
            "answer": "int"
          },
          {
            "type": "short answer",
            "question": "At what price in GBP would you consider the product to be a bargain? ",
            "answer": "int"
          }
        ]


responses = []
for question in survey_questions:
    prompt = question["question"]+"\nResponse schema:\n"+json.dumps(question)
    response=agent.chat(query=prompt)
    agent.st_memory_length()
    response_data=json.loads(response)
    responses.append(response_data)

for response in responses:
    print(response)
    print("\n")

import app.internal.response_agent as response_agent
import app.internal.demgen as demgen
import json
import app.internal.simulation as simulation


demographic= {
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


survey = {
      "name": "PSM Scenario 3 Demographic 3",
      "description": "The product is a smartphone with the following features:\nDisplay: 6.8-inch QHD+ Dynamic AMOLED with high refresh rate\nProcessor: Snapdragon Gen3\nCamera: quad-camera with 108MP main sensor, periscope zoom\nBattery: 5,500mAh with super fast charging, wireless charging\nConnectivity: 5G, Wi-Fi 6E, Ultra-wide-band\nStorage: 25G6B/512GB/1TB expandable\nRAM: 12GB/16GB\nOther: Stainless steel frame with Gorilla glass front and back build, IP68, built in AI smart features",    
      "questions": [
        {
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
      }



generator=demgen.Demographic_Generator(demo=demographic, n_of_results=1)
demo_data=generator.generate_demographic_dataset()
demo_data=demo_data[0]


simulation_result=simulation.simulate(survey, demo_data)
print(simulation_result)
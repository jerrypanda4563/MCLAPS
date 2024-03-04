import app.internal.response_agent as response_agent
import app.internal.demgen as demgen
import json
import app.internal.simulation as simulation
from app.internal import agent_data
import time


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


example_string = """Once upon a time, in a land far away, nestled between rolling hills and vast forests, there lay a small village known for its vibrant fields and a river that sparkled under the sun's gentle gaze. This village was home to a young girl named Lila, who lived with her grandmother in a cozy cottage at the edge of the woods. Lila was adventurous, kind-hearted, and had a curious spirit that often led her to explore the mysteries of the forest.

One day, while wandering deeper into the woods than she had ever dared before, Lila stumbled upon a hidden glade, where sunlight danced through the leaves and illuminated a clearing that seemed untouched by time. In the center of this glade was a magnificent tree, its branches heavy with golden fruits that shone like tiny suns. Lila had heard tales of the fabled Tree of Eternity, a mystical plant that bore fruits with the power to grant one's heart's deepest desires, but she had always believed it to be just a story.

As she approached the tree, she noticed an old, intricately carved box at its base. Driven by curiosity, Lila opened the box and found a single, shimmering seed lying within. The moment her fingers brushed against the seed, a gentle voice echoed through the glade, "To the one who finds this seed, know that it holds the power to change the world. But with great power comes great responsibility. Use it wisely, for its effects will ripple through the ages."

Lila was taken aback. She had never believed in magic or fables, yet the reality of it was right before her eyes. Clutching the seed tightly, she made her way back to the village, pondering the weight of the choice that lay before her. She knew that such power could bring prosperity to her village, heal the sick, or bring about endless summers. Yet, the more she thought about it, the more she realized that the seed's true power lay not in granting wishes, but in inspiring hope and change through one's own actions.

Determined to make a difference, Lila decided to plant the seed in the village square. Days turned into weeks, and weeks into months, and slowly, the seed grew into a towering tree, unlike any other. It bore no golden fruits, nor did it possess magical properties. Instead, it became a symbol of unity for the village. People from all walks of life came to marvel at the tree, and under its sprawling branches, they shared stories, dreams, and laughter. The tree brought the community together, fostering a spirit of cooperation and kindness that spread throughout the land.

Years passed, and Lila grew to become a wise and respected leader. The village flourished like never before, not because of magic, but because of the collective efforts of its people. The Tree of Eternity, as it came to be known, stood as a testament to the power of hope, the importance of community, and the belief that even the smallest actions can lead to great change.

And so, Lila's story became a legend, passed down through generations, reminding all who heard it of the magic that lies in believing in oneself and in the power of coming together for a common good. The village continued to thrive, and the tree remained, evergreen and enduring, a beacon of light in a world that, too often, forgot the strength found in unity and the simple act of planting a seed of hope.

And they all lived happily ever after, in a world that was a little bit better, because one girl dared to believe in the power of change."""


data = agent_data_copy.AgentData()
start_time = time.time()
data.add_data_str(example_string)
end_time = time.time()
print(f"Time taken to add data: {end_time - start_time} seconds")

start_time = time.time()
query = data.query("What is the moral of the story?")
end_time = time.time()
print(f"Time taken to query data: {end_time - start_time} seconds")
for string in query:
    print(string)
    print("\n\n\n")
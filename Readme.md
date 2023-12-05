# MCLAPS


## Runing the API locally

1. create a .env file inside app with the following:
```
OPEN-AI-API-KEY = 
MONGO_URI = 
REDIS_URI = 


```

2. run with uvicorn
```shell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

3. access endpoints via localhost fastapi interface

```shell
http://localhost:8000/docs#/
```

4. sample request body
```shell
{
    "survey_model": {
        "name": "Pricing Research on a New Fitness Tracker",
        "description": "Survey for Pricing Research on a New Fitness Tracker",
        "questions": [
            {
                "type": "short answer",
                "question": "Age:"
            },
            {
                "type": "multiple choice",
                "question": "Gender:",
                "choices": ["Male", "Female", "Non-Binary"]
            },
            {
                "type": "short answer",
                "question": "Occupation:"
            },
            {
                "type": "multiple choice",
                "question": "Do you currently use a fitness tracker?",
                "choices": ["Yes", "No"]
            },
            {
                "type": "short answer",
                "question": "If yes, which brand/model of fitness tracker do you use?"
            },
            {
                "type": "checkboxes",
                "question": "What features do you most value in a fitness tracker?",
                "choices": [
                    "Activity tracking (steps, distance, calories burned, etc.)", 
                    "Heart rate monitoring",
                    "Sleep tracking", 
                    "GPS navigation", 
                    "Smartphone notifications", 
                    "Battery life",
                    "Aesthetic/design"
                ]
            },
            {
                "type": "linear scale",
                "question": "At a price of $50, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
                "min_value": 1,
                "max_value": 10
            },
            {
                "type": "linear scale",
                "question": "At a price of $100, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
                "min_value": 1,
                "max_value": 10
            },
            {
                "type": "linear scale",
                "question": "At a price of $150, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
                "min_value": 1,
                "max_value": 10
            },
            {
                "type": "linear scale",
                "question": "At a price of $200, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
                "min_value": 1,
                "max_value": 10
            },
            {
                "type": "linear scale",
                "question": "At a price of $250, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
                "min_value": 1,
                "max_value": 10
            },
            {
                "type": "linear scale",
                "question": "At a price of $300, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
                "min_value": 1,
                "max_value": 10
            },
            {
                "type": "linear scale",
                "question": "At a price of $350, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
                "min_value": 1,
                "max_value": 10
            },
            {
                "type": "linear scale",
                "question": "At a price of $400, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
                "min_value": 1,
                "max_value": 10
            },
            {
                "type": "linear scale",
                "question": "At a price of $500, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
                "min_value": 1,
                "max_value": 10
            },
            {
                "type": "linear scale",
                "question": "At a price of $600, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
                "min_value": 1,
                "max_value": 10
            }
        ]
    },
    "demographic_model": {
        "age": "20-40",
        "income_level": "£60000 to £80000",
        "country_of_residence": "United Kingdom",
        "hobbies_and_interests": "Interest in fitness, wellness, and technology",
        "physical_activity_levels": "Moderate to high",
        "social_media_usage": "Moderate to high",
        "general_health_status": "Good to excellent",
        "gender_identity": null,
        "marital_status": null,
        "sexual_orientation": null,
        "nationality": null,
        "state_province": null,
        "city": null,
        "rural_or_urban": null,
        "type_of_residence": null,
        "length_of_residence": null,
        "field_of_study": null,
        "occupation": null,
        "social_class": null,
        "employment_status": null,
        "home_ownership": null,
        "ethnicity": null,
        "languages_spoken": null,
        "religion": null,
        "cultural_practices": null,
        "immigration_status": null,
        "shopping_preferences": null,
        "dietary_preferences": null,
        "travel_habits": null,
        "alcohol_tobacco_use": null,
        "technology_usage": null,
        "family_structure": null,
        "household_size": null,
        "pet_ownership": null,
        "relationship_status": null,
        "caregiving_responsibilities": null,
        "disabilities_or_chronic_illnesses": null,
        "mental_health_status": null,
        "health_insurance_status": null,
        "access_to_healthcare": null,
        "political_affiliation": null,
        "voting_behavior": null,
        "political_engagement": null
    }
}
```
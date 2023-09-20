import agent
import data_services
import demgen
import json

### class simulate implementing exception handling, creates a single instances of demo and agent, input is survey plus all dem param
class simulate():
    def __init__(self, survey: list, 
                 gender_identity=None, age=None, date_of_birth=None,
                marital_status=None, sexual_orientation=None, nationality=None, citizenship=None,
                country_of_residence=None, state_province=None, city=None,
                rural_or_urban=None, type_of_residence=None, length_of_residence=None,
                level_of_education=None, field_of_study=None, occupation=None, income_level=None,
                social_class=None, employment_status=None, home_ownership=None, ethnicity=None,
                languages_spoken=None, religion=None, cultural_practices=None,
                immigration_status=None, hobbies_and_interests=None, shopping_preferences=None,
                dietary_preferences=None, physical_activity_levels=None, social_media_usage=None,
                travel_habits=None, alcohol_tobacco_use=None, technology_usage=None,
                family_structure=None, household_size=None, pet_ownership=None,
                relationship_status=None, caregiving_responsibilities=None,
                general_health_status=None, disabilities_or_chronic_illnesses=None,
                mental_health_status=None, health_insurance_status=None,
                access_to_healthcare=None, political_affiliation=None, voting_behavior=None,
                political_engagement=None):
        #input
        self.survey=survey  #must be a list of dict
        #temp memory for storing output
        self.demographic_data={}
        self.responses=[]
        #demo parameters
        self.gender_identity=gender_identity
        self.age=age
        self.date_of_birth=date_of_birth
        self.marital_status=marital_status
        self.sexual_orientation=sexual_orientation
        self.nationality=nationality
        self.country_of_residence=country_of_residence
        self.state_province=state_province
        self.city=city
        self.rural_or_urban=rural_or_urban
        self.type_of_residence=type_of_residence
        self.length_of_residence=length_of_residence
        self.level_of_education=level_of_education
        self.field_of_study=field_of_study
        self.occupation=occupation
        self.income_level=income_level
        self.social_class=social_class 
        self.employment_status=employment_status
        self.home_ownership=home_ownership
        self.ethnicity=ethnicity
        self.languages_spoken=languages_spoken
        self.religion=religion
        self.cultural_practices=cultural_practices
        self.immigration_status=immigration_status
        self.hobbies_and_interests=hobbies_and_interests
        self.shopping_preferences=shopping_preferences
        self.dietary_preferences=dietary_preferences 
        self.physical_activity_levels=physical_activity_levels
        self.social_media_usage=social_media_usage
        self.travel_habits=travel_habits
        self.alcohol_tobacco_use=alcohol_tobacco_use
        self.technology_usage=technology_usage
        self.family_structure=family_structure
        self.household_size=household_size
        self.pet_ownership=pet_ownership
        self.relationship_status=relationship_status
        self.caregiving_responsibilities=caregiving_responsibilities
        self.general_health_status=general_health_status
        self.disabilities_or_chronic_illnesses=disabilities_or_chronic_illnesses
        self.mental_health_status=mental_health_status
        self.health_insurance_status=health_insurance_status
        self.access_to_healthcare=access_to_healthcare
        self.political_affiliation=political_affiliation
        self.voting_behavior=voting_behavior
        self.political_engagement=political_engagement
        

    def update_demographic_parameters(self, params):
        self.gender_identity = params.get("Gender Identity", self.gender_identity)
        self.age = params.get("Age", self.age)
        self.date_of_birth = params.get("Date of Birth", self.date_of_birth)
        self.marital_status = params.get("Marital Status", self.marital_status)
        self.sexual_orientation = params.get("Sexual Orientation", self.sexual_orientation)
        self.nationality = params.get("Nationality", self.nationality)
        self.country_of_residence = params.get("Country of Residence", self.country_of_residence)
        self.state_province = params.get("State/Province", self.state_province)
        self.city = params.get("City", self.city)
        self.rural_or_urban = params.get("Rural or Urban", self.rural_or_urban)
        self.type_of_residence = params.get("Type of Residence", self.type_of_residence)
        self.length_of_residence = params.get("Length of Residence", self.length_of_residence)
        self.level_of_education = params.get("Level of Education", self.level_of_education)
        self.field_of_study = params.get("Field of Study", self.field_of_study)
        self.occupation = params.get("Occupation", self.occupation)
        self.income_level = params.get("Income Level", self.income_level)
        self.social_class = params.get("Social Class", self.social_class)
        self.employment_status = params.get("Employment Status", self.employment_status)
        self.home_ownership = params.get("Home Ownership", self.home_ownership)
        self.ethnicity = params.get("Ethnicity", self.ethnicity)
        self.languages_spoken = params.get("Language(s) Spoken", self.languages_spoken)
        self.religion = params.get("Religion", self.religion)
        self.cultural_practices = params.get("Cultural Practices", self.cultural_practices)
        self.immigration_status = params.get("Immigration Status", self.immigration_status)
        self.hobbies_and_interests = params.get("Hobbies and Interests", self.hobbies_and_interests)
        self.shopping_preferences = params.get("Shopping Preferences", self.shopping_preferences)
        self.dietary_preferences = params.get("Dietary Preferences", self.dietary_preferences)
        self.physical_activity_levels = params.get("Physical Activity Levels", self.physical_activity_levels)
        self.social_media_usage = params.get("Social Media Usage", self.social_media_usage)
        self.travel_habits = params.get("Travel Habits", self.travel_habits)
        self.alcohol_tobacco_use = params.get("Alcohol and Tobacco Use", self.alcohol_tobacco_use)
        self.technology_usage = params.get("Technology Usage", self.technology_usage)
        self.family_structure = params.get("Family Structure", self.family_structure)
        self.household_size = params.get("Household Size", self.household_size)
        self.pet_ownership = params.get("Pet Ownership", self.pet_ownership)
        self.relationship_status = params.get("Relationship Status", self.relationship_status)
        self.caregiving_responsibilities = params.get("Caregiving Responsibilities", self.caregiving_responsibilities)
        self.general_health_status = params.get("General Health Status", self.general_health_status)
        self.disabilities_or_chronic_illnesses = params.get("Disabilities or Chronic Illnesses", self.disabilities_or_chronic_illnesses)
        self.mental_health_status = params.get("Mental Health Status", self.mental_health_status)
        self.health_insurance_status = params.get("Health Insurance Status", self.health_insurance_status)
        self.access_to_healthcare = params.get("Access to Healthcare", self.access_to_healthcare)
        self.political_affiliation = params.get("Political Affiliation", self.political_affiliation)
        self.voting_behavior = params.get("Voting Behavior", self.voting_behavior)
        self.political_engagement = params.get("Political Engagement", self.political_engagement)

    
    def run(self):
        max_retries = 3  # Set maximum number of retries
        
        #Retry block for generating demographic
        for _ in range(max_retries):
            try:
                demo=demgen.generate_demographic(gender_identity=self.gender_identity, age=self.age, date_of_birth=self.date_of_birth,
                                            marital_status=self.marital_status, sexual_orientation=self.sexual_orientation, nationality=self.nationality,
                                            country_of_residence=self.country_of_residence, state_province=self.state_province, city=self.city, 
                                            rural_or_urban=self.rural_or_urban, type_of_residence=self.type_of_residence, length_of_residence=self.length_of_residence, 
                                            level_of_education=self.level_of_education, field_of_study=self.field_of_study, occupation=self.occupation, income_level=self.income_level, 
                                            social_class=self.social_class, employment_status=self.employment_status, home_ownership=self.home_ownership, ethnicity=self.ethnicity,
                                            languages_spoken=self.languages_spoken, religion=self.religion, cultural_practices=self.cultural_practices, immigration_status=self.immigration_status,
                                            hobbies_and_interests=self.hobbies_and_interests, shopping_preferences=self.shopping_preferences, dietary_preferences=self.dietary_preferences,
                                            physical_activity_levels=self.physical_activity_levels, social_media_usage=self.social_media_usage, travel_habits=self.travel_habits, 
                                            alcohol_tobacco_use=self.alcohol_tobacco_use, technology_usage=self.technology_usage, family_structure=self.family_structure, household_size=self.household_size, 
                                            pet_ownership=self.pet_ownership, relationship_status=self.relationship_status, caregiving_responsibilities=self.caregiving_responsibilities, general_health_status=self.general_health_status,
                                            disabilities_or_chronic_illnesses=self.disabilities_or_chronic_illnesses, mental_health_status=self.mental_health_status, health_insurance_status=self.health_insurance_status,
                                            access_to_healthcare=self.access_to_healthcare, political_affiliation=self.political_affiliation, voting_behavior=self.voting_behavior, political_engagement=self.political_engagement)
                break
            except Exception as e:
                print(f"Error in generating demographic (Attempt {_ + 1}): {e}")
        else:  # This else block is executed if the loop ends without a break
            print("Maximum retries reached for generating demographic.")
            return
        #End of retry block
        
        #Retry block for loading demographic data
        for _ in range(max_retries):
            try:
                self.demographic_data.update(json.loads(demo))
                break
            except json.JSONDecodeError:
                print(f"Error decoding the generated demographic JSON (Attempt {_ + 1}).")
            except Exception as e:
                print(f"Error in updating demographic data (Attempt {_ + 1}): {e}")
        else:
            print("Maximum retries reached for updating demographic data.")
            return
        #End of block


        simulator = agent.Agent("You are a person with the following demographic characteristics expressed as a json dictionary:" + demo + "\nRespond to the following survey questions expressed as a list of json dictionaries by replacing null values with your answer. Your output must maintain the same data structure as the input.")

        for question in self.survey:
            prompt = json.dumps(question)

            #Retry block for generating response
            for _ in range(max_retries):
                try:
                    response = simulator.chat(prompt)
                    break
                except Exception as e:
                    print(f"Error in chat simulation for question (Attempt {_ + 1}): {question}. Error: {e}")
            else:
                print(f"Maximum retries reached for question: {question}. Skipping to next question.")
                continue
            #End of block
            
            #Retry block for loading response data
            for _ in range(max_retries):
                try:
                    response_data = json.loads(response)
                    self.responses.append(response_data)
                    break
                except json.JSONDecodeError:
                    print(f"Error decoding the response JSON (Attempt {_ + 1}).")
                except Exception as e:
                    print(f"Error processing response data (Attempt {_ + 1}): {e}")
            else:
                print(f"Failed to process response after {max_retries} attempts. Skipping.")
            #End of block









    









    
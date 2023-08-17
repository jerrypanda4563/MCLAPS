import agent
import data_services
import demgen
import json




class Simulation():

    def __init__(self,survey,filename):                                 
        self.filename=filename
        self.survey=survey
        self.response_error=[]
        self.demographic_error=[]
        self.n_success=0
        self.n_failure=0
        self.consecutive_failures = 0
        self.raw_demographics=[]
        self.raw_responses=[]
        
        #Default demographic Parameters
        self.gender_identity=None
        self.age=None
        self.date_of_birth=None
        self.marital_status=None
        self.sexual_orientation=None
        self.nationality=None
        self.citizenship=None
        self.country_of_residence=None
        self.state_province=None
        self.city=None
        self.rural_or_urban=None
        self.type_of_residence=None
        self.length_of_residence=None
        self.level_of_education=None
        self.field_of_study=None
        self.occupation=None
        self.income_level=None
        self.social_class=None 
        self.employment_status=None
        self.home_ownership=None
        self.ethnicity=None
        self.languages_spoken=None
        self.religion=None
        self.cultural_practices=None
        self.immigration_status=None
        self.hobbies_and_interests=None
        self.shopping_preferences=None
        self.dietary_preferences=None 
        self.physical_activity_levels=None
        self.social_media_usage=None
        self.travel_habits=None
        self.alcohol_tobacco_use=None
        self.technology_usage=None
        self.family_structure=None
        self.household_size=None
        self.pet_ownership=None
        self.relationship_status=None
        self.caregiving_responsibilities=None
        self.general_health_status=None
        self.disabilities_or_chronic_illnesses=None
        self.mental_health_status=None
        self.health_insurance_status=None
        self.access_to_healthcare=None
        self.political_affiliation=None
        self.voting_behavior=None
        self.political_engagement=None

    def demographic_parameters(self,gender_identity=None, age=None, date_of_birth=None,
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
        self.gender_identity=gender_identity
        self.age=age
        self.date_of_birth=date_of_birth
        self.marital_status=marital_status
        self.sexual_orientation=sexual_orientation
        self.nationality=nationality
        self.citizenship=citizenship
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

    def simulate(self,n_of_runs):
        #creating simulation files
        self.survey.create_csv('./simulations/'+self.filename+'.csv')        
        data_services.create_demographic_csv('./simulations/'+self.filename+'_demographics.csv')
        questions=self.survey.to_json()      
        #simulation loop
        while True:
            if self.n_success >= n_of_runs:
                break
            try:
                for i in range(n_of_runs - self.n_success):
                    
                    #creating demographic profile
                    try:
                        demo=demgen.generate_demographic(gender_identity=self.gender_identity, age=self.age, date_of_birth=self.date_of_birth,
                                    marital_status=self.marital_status, sexual_orientation=self.sexual_orientation, nationality=self.nationality, citizenship=self.citizenship,
                                    country_of_residence=self.country_of_residence, state_province=self.state_province, city=self.citizenship,
                                    rural_or_urban=self.rural_or_urban, type_of_residence=self.type_of_residence, length_of_residence=self.length_of_residence,
                                    level_of_education=self.level_of_education, field_of_study=self.field_of_study, occupation=self.occupation, income_level=self.income_level,
                                    social_class=self.social_class, employment_status=self.employment_status, home_ownership=self.home_ownership, ethnicity=self.ethnicity,
                                    languages_spoken=self.languages_spoken, religion=self.religion, cultural_practices=self.cultural_practices,
                                    immigration_status=self.immigration_status, hobbies_and_interests=self.hobbies_and_interests, shopping_preferences=self.shopping_preferences,
                                    dietary_preferences=self.dietary_preferences, physical_activity_levels=self.physical_activity_levels, social_media_usage=self.social_media_usage,
                                    travel_habits=self.travel_habits, alcohol_tobacco_use=self.alcohol_tobacco_use, technology_usage=self.technology_usage,
                                    family_structure=self.family_structure, household_size=self.household_size, pet_ownership=self.pet_ownership,
                                    relationship_status=self.relationship_status, caregiving_responsibilities=self.caregiving_responsibilities,
                                    general_health_status=self.general_health_status, disabilities_or_chronic_illnesses=self.disabilities_or_chronic_illnesses,
                                    mental_health_status=self.mental_health_status, health_insurance_status=self.health_insurance_status,
                                    access_to_healthcare=self.access_to_healthcare, political_affiliation=self.political_affiliation, voting_behavior=self.voting_behavior,
                                    political_engagement=self.political_engagement)
                        self.raw_demographics.append(demo)
                        demo_json=data_services.extract_json_content(demo)
                    except Exception as e:
                        self.n_failure+=1
                        self.consecutive_failures += 1
                        print(f"An error occurred while generating demographic data: {e}. Skipping this iteration...")
                        if self.consecutive_failures >= 5:
                            print("Too many consecutive failures. Stopping the simulation.")
                            data_services.clean_up_csv('./simulations/'+self.filename+'.csv')
                            data_services.clean_up_csv('./simulations/'+self.filename+'_demographics.csv')
                            return
                        continue

                    try:
                        demo_data=json.loads(demo_json)
                    except Exception as e:
                        self.demographic_error.append(demo_json)
                        self.n_failure+=1
                        self.consecutive_failures += 1
                        print(f"An error occurred while parsing demographic data: {e}. Skipping this iteration...")
                        if self.consecutive_failures >= 5:
                            print("Too many consecutive failures. Stopping the simulation.")
                            data_services.clean_up_csv('./simulations/'+self.filename+'.csv')
                            data_services.clean_up_csv('./simulations/'+self.filename+'_demographics.csv')
                            return
                        continue

                    #simulating survey response
                    respondant=agent.Agent(demo_json)
                    try:
                        response=respondant.chat(questions)
                        self.raw_responses.append(response)
                        response_json=data_services.extract_json_content(response)
                    except Exception as e:
                        self.n_failure+=1
                        self.consecutive_failures += 1
                        print(f"An error occurred while simulating survey response: {e}. Skipping this iteration...")
                        if self.consecutive_failures >= 5:
                            print("Too many consecutive failures. Stopping the simulation.")
                            data_services.clean_up_csv('./simulations/'+self.filename+'.csv')
                            data_services.clean_up_csv('./simulations/'+self.filename+'_demographics.csv')
                            return
                        continue


                    try:
                        response_data=json.loads(response_json)
                    except Exception as e:
                        self.response_error.append(response_json)
                        self.n_failure+=1
                        self.consecutive_failures += 1
                        print(f"An error occurred while parsing response data: {e}. Skipping this iteration...")
                        if self.consecutive_failures >= 5:
                            print("Too many consecutive failures. Stopping the simulation.")
                            data_services.clean_up_csv('./simulations/'+self.filename+'.csv')
                            data_services.clean_up_csv('./simulations/'+self.filename+'_demographics.csv')
                            return
                        continue

                    #appending data
                    try:
                        data_services.append_response('./simulations/'+self.filename+'.csv',response_data)
                    except Exception as e:
                        self.n_failure+=1
                        self.response_error.append(response_json)
                        self.consecutive_failures += 1
                        print(f"An error occurred while appending response data: {e}. Skipping this iteration...")
                        if self.consecutive_failures >= 5:
                            print("Too many consecutive failures. Stopping the simulation.")
                            data_services.clean_up_csv('./simulations/'+self.filename+'.csv')
                            data_services.clean_up_csv('./simulations/'+self.filename+'_demographics.csv')
                            return
                        continue  

                    try:
                        data_services.append_demographic('./simulations/'+self.filename+'_demographics.csv',demo_data)
                    except Exception as e:
                        self.n_failure+=1
                        self.demographic_error.append(demo_json)
                        self.consecutive_failures += 1
                        print(f"An error occurred while appending demographic data: {e}. Skipping this iteration...")
                        if self.consecutive_failures >= 5:
                            print("Too many consecutive failures. Stopping the simulation.")
                            data_services.clean_up_csv('./simulations/'+self.filename+'.csv')
                            data_services.clean_up_csv('./simulations/'+self.filename+'_demographics.csv')
                            return
                        continue  

                    #recording successful run
                    self.n_success += 1  
                    self.consecutive_failures = 0  # reset the consecutive failures counter
                    print("Demographic and response data successfully appended")
                    if self.n_success >= n_of_runs:
                        data_services.clean_up_csv('./simulations/'+self.filename+'.csv')
                        data_services.clean_up_csv('./simulations/'+self.filename+'_demographics.csv')
                        print(f"Simulation Complete")
                        break

                #indicating simulation completion
                if self.n_success >= n_of_runs:
                    print(f"Simulation Complete")
                    data_services.clean_up_csv('./simulations/'+self.filename+'.csv')
                    data_services.clean_up_csv('./simulations/'+self.filename+'_demographics.csv')
                    break  

            #returning general error
            except Exception as e:
                self.n_failure+=1
                self.consecutive_failures += 1
                print(f"An unknown error occurred: {e}. Retrying...")
                if self.consecutive_failures >= 5:
                    data_services.clean_up_csv('./simulations/'+self.filename+'.csv')
                    data_services.clean_up_csv('./simulations/'+self.filename+'_demographics.csv')
                    print("Too many consecutive failures. Stopping the simulation.")
                    return


    def show_performance(self):
        print(f'Number of successful runs:'+str(self.n_success))
        print(f'Number of failures:'+str(self.n_failure))

    def show_demographic_error(self):
        with open(self.filename + '_demographic_errors.txt', 'w') as f:
            print(f'Demographic data errors', file=f)
            print("\n")
            for d_err in self.demographic_error:
                print(d_err, file=f)
                print("\n")

    def show_response_error(self):
        with open(self.filename + '_response_errors.txt', 'w') as f:
            print(f'Response data errors', file=f)
            print("\n")
            for d_err in self.response_error:
                print(d_err, file=f)
                print("\n")
    
    def show_raw_demographics(self):
        with open(self.filename + '_raw_demographics.txt', 'w') as f:
            print(f'Raw demographics data', file=f)
            print("\n")
            for dem_raw in self.raw_demographics:
                print(dem_raw, file=f)
                print("\n")

    def show_raw_responses(self):
        with open(self.filename + '_raw_responses.txt', 'w') as f:
            print(f'Raw responses data', file=f)
            print("\n")
            for res_raw in self.raw_responses:
                print(res_raw, file=f)
                print("\n")
    







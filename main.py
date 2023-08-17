import survey
import simulation
import time


#Juanjuan Sim 1
elderly_survey=survey.Survey()
elderly_survey.add_multiple_choice_question('Please select your age range',['60-64','65-70','71-74','75-80','81-84','85 and above'])
elderly_survey.add_multiple_choice_question('Please select your gender',['Male','Female','Prefer not to say','Other:'])
elderly_survey.add_multiple_choice_question('If you are in London, please select your borough in London',['Barking and Dagenham','Barnet','Bexley','Brent','Bromley','Camden','City of London','Corydon','Ealing','Enfield','Greenwich','Hackney','Hammersmith and Fulham','Haringey','Harrow','Havering','Hillingdon','Hounslow','Islington','Kensington and Chelsea','Kingston upon Thames','Lambeth','Lewisham','Merton','Newham','Redbridge','Richmond upon Thames','Southwark','Sutton','Tower Hamlets','Waltham Forest','Wandsworth','Westminster','Other:'])
elderly_survey.add_multiple_choice_question('Please select your current living situation',['Living alone','Living with spouse/partner','Living with family','Living in a care home','Other:'])
elderly_survey.add_multiple_choice_question('Are you currently using any kind of elder care services?',['Yes','No'])
elderly_survey.add_short_answer_question('If you are using elder care services, what provider and services are you using?')
elderly_survey.add_linear_scale_question('How would you rate your overall quality of life in retirement?',1,7)
elderly_survey.add_checkboxes_question('Which of the following challenges do you regularly face? (Select all that applies)',['Mobility issues','Access to healthcare','Loneliness','Financial difficulties','Lack of assistance with daily tasks','Other:'])
elderly_survey.add_linear_scale_question('On a scale of 1-7, how would you rate your current level of social interaction and community involvement?',1,7)
elderly_survey.add_checkboxes_question('What are your primary unmet needs?',['Healthcare','Companionship','Assistance with daily tasks','Financial Support','Other:'])
elderly_survey.add_multiple_choice_question('Would you be open to receiving care or assistance from university students?',['Yes','No','Maybe'])
elderly_survey.add_checkboxes_question('What tasks would you feel comfortable letting a university student assist you with?',['Grocery shopping','House cleaning','Medical appointments','social outings','technology tutoring','Other:'])
elderly_survey.add_linear_scale_question('On a scale of 1-7, how concerned are you about interacting with university students in a caregiving context?',1,7)
elderly_survey.add_multiple_choice_question('How would you prefer to connect with potential student caregivers?',['Online platform','Phone','In-person meetings','Other:'])
elderly_survey.add_checkboxes_question('What qualities would you want student caregivers to have? (Select all that apply)',['Patience','Experience with elder care','Good communication skills','Reliability','Other:'])
elderly_survey.add_long_answer_question('Please share any other thoughts or concerns you have about the idea of an intergenerational elder care platform.')
elderly_survey.show()
#Demographic Parameters 
#gender_identity=None
#age=None
#date_of_birth=None
#marital_status=None
#sexual_orientation=None
#nationality=None
#citizenship=None
#country_of_residence=None
#state_province=None
#city=None
#rural_or_urban=None
#type_of_residence=None
#length_of_residence=None
#level_of_education=None
#field_of_study=None
#occupation=None
#income_level=None
#social_class=None 
#employment_status=None
#home_ownership=None
#ethnicity=None
#languages_spoken=None
#religion=None
#cultural_practices=None
#immigration_status=None
#hobbies_and_interests=None
#shopping_preferences=None
#dietary_preferences=None 
#physical_activity_levels=None
#social_media_usage=None
#travel_habits=None
#alcohol_tobacco_use=None
#technology_usage=None
#family_structure=None
#household_size=None
#pet_ownership=None
#relationship_status=None
#caregiving_responsibilities=None
#general_health_status=None
#disabilities_or_chronic_illnesses=None
#mental_health_status=None
#health_insurance_status=None
#access_to_healthcare=None
#political_affiliation=None
#voting_behavior=None
#political_engagement=None


MaMa_elder=simulation.Simulation(elderly_survey,"MaMa")
MaMa_elder.demographic_parameters(age='65-90',country_of_residence='United Kingdom')

start_time = time.time() ##00:32 start
MaMa_elder.simulate(n_of_runs=60)
end_time = time.time()

MaMa_elder.show_performance()

runtime=end_time-start_time
print(runtime)

MaMa_elder.show_demographic_error()
MaMa_elder.show_response_error()
MaMa_elder.show_raw_demographics()
MaMa_elder.show_raw_responses()










#Juanjuan Sim 2
technology_survey=survey.Survey()
technology_survey.add_multiple_choice_question('Please select your age range:',['71-74','75-80','81-84','85 and above'])
technology_survey.add_multiple_choice_question('Please select your gender:',['Male','Female','Prefer not to say','Other:'])
technology_survey.add_multiple_choice_question('If you are in London, please select your borough in London:',['Barking and Dagenham','Barnet','Bexley','Brent','Bromley','Camden','City of London','Corydon','Ealing','Enfield','Greenwich','Hackney','Hammersmith and Fulham','Haringey','Harrow','Havering','Hillingdon','Hounslow','Islington','Kensington and Chelsea','Kingston upon Thames','Lambeth','Lewisham','Merton','Newham','Redbridge','Richmond upon Thames','Southwark','Sutton','Tower Hamlets','Waltham Forest','Wandsworth','Westminster','Other:'])
technology_survey.add_multiple_choice_question('Please select your current living situation',['Living alone','Living with spouse/partner','Living with family','Living in a care home','Other:'])
technology_survey.add_checkboxes_question('What types of technology do you currently use? (Select all that apply)',['Smartphone','Computer (Desktop/Laptop)','Tablet','Smart TV','Other:'])
technology_survey.add_linear_scale_question('How comfortable are you with using the technology you own?',1,7)
technology_survey.add_checkboxes_question('Which channels do you currently use to learn new technology? (Select all that apply)',['Public Libraries and Community Centers','Local Adult Education Programs','Volunteer Organizations','Online Tutorials and Courses','Books or manuals','Family and Friends','Tech Companies and Customer service','There is no channel','Other:'])
technology_survey.add_long_answer_question('Have you ever paid to learn technology? If so, what fee-based platforms have you used? What courses have you taken?')
technology_survey.add_checkboxes_question('What kinds of activities do you do using technology? (Select all that apply)',['Communicating with friends or family (email, messaging, video calls, etc.)','Entertainment (Watching movies, TV shows, Listening to music, reading news, information, etc.)','Online Shopping and Food Delivery','Banking and Bill Payments','Healthcare (Book medical appointments, order prescriptions, consultations with healthcare providers, etc.)','Learning','Travel and Navigation','Smart Home Devices','Community Engagement','Other:'])
technology_survey.add_checkboxes_question('What challenges do you face when using technology? (Select all that apply)',['Understanding how to use new apps or features','Troubleshooting issues or errors','Navigating the internet safely','Keeping track of passwords','Other:'])
technology_survey.add_linear_scale_question('On a scale of 1-7, How open are you to learning new technologies?',1,7)
technology_survey.add_checkboxes_question('What areas would you like assistance with in terms of technology? (Select all that apply)',['Learning how to use new apps or features','Troubleshooting issues or errors','Navigating the internet safely','Managing passwords','Other:'])
technology_survey.add_multiple_choice_question('Would you prefer in-person assistance or remote assistance (e.g., over the phone or video call)?',['In-person assistance','Remote assistance','No preference'])
technology_survey.add_long_answer_question('How do you think improved technology skills could impact your daily life?')




MaMa_technology=simulation.Simulation(technology_survey,"MaMa_tech")
MaMa_technology.demographic_parameters(age='71-90',country_of_residence='United Kingdom')

start_time = time.time() ##13:00
MaMa_technology.simulate(n_of_runs=60)
end_time = time.time()

MaMa_technology.show_performance()

runtime=end_time-start_time
print(runtime)

MaMa_technology.show_demographic_error()
MaMa_technology.show_response_error()
MaMa_technology.show_raw_demographics()
MaMa_technology.show_raw_responses()










#Nikhil Sim 1
swyftin_survey=survey.Survey()
swyftin_survey.add_multiple_choice_question('How frequently do you travel in a year?',['Less than 5 times','5-10 times','11-15 times','16-20 times','More than 20 times'])
swyftin_survey.add_multiple_choice_question('What kind of accomodation do you prefer?',['1 star','2 star','3 star','4 star','5 star'])
swyftin_survey.add_linear_scale_question('How satisfied are you interacting with human concierge for hotel related queries?',0,5)
swyftin_survey.add_linear_scale_question('How comfortable do you feel about interacting with AI systems while traveling?',0,5)
swyftin_survey.add_multiple_choice_question('Have you ever used an AI system during your travels?',['Yes','No'])
swyftin_survey.add_checkboxes_question('If yes, please select the AI systems you have used (Select all that apply):',['Chatbots','Virtual assistants','Automated check-in kiosks','Smart luggage','Other:','N/A'])
swyftin_survey.add_linear_scale_question('How satisfied were you with the AI systems you have used during your travels?',0,5)
swyftin_survey.add_checkboxes_question('What aspects of AI systems during your travels do you find could be most helpful? (Select all that apply)',['Interacting with hotel concierge','Recommendations for activities and attractions','Flight and hotel recommendations','Language translation','Navigation assistance','Other:'])
swyftin_survey.add_multiple_choice_question('Do you think AI systems can improve your overall travel experience?',['Yes','No'])
swyftin_survey.add_linear_scale_question('How comfortable are you with AI systems collecting and using your personal data during your travels?',0,5)
swyftin_survey.add_linear_scale_question('How likely are you to recommend AI systems to other travelers?',0,5)
swyftin_survey.add_long_answer_question('In your opinion, what improvements can be made to AI systems in the travel industry?')
swyftin_survey.add_multiple_choice_question('Would you prefer human interaction over AI systems while traveling or staying at a property?',['Yes','No'])
swyftin_survey.add_linear_scale_question('How important is it for AI systems to understand and respond to your emotions while traveling?',0,5)
swyftin_survey.add_short_answer_question('Which city/country are you from?')
swyftin_survey.add_multiple_choice_question('What is your gender?',['Female','Male','Non-binary','Transgender','Prefer not to say','Other:'])
swyftin_survey.add_multiple_choice_question('What is your age group?',['18-24','25-34','35-44'])


swyftin=simulation.Simulation(swyftin_survey,"Swyftin")
swyftin.demographic_parameters(age='24-40',country_of_residence='India',nationality='Indian',ethnicity='Indian',employment_status=['Full-time','Part-time'])


start_time = time.time() ##17:40
swyftin.simulate(n_of_runs=10)
end_time = time.time()


print(f'Runtime:' +str(end_time-start_time))

swyftin.show_performance()
swyftin.show_raw_demographics()
swyftin.show_raw_responses()
swyftin.show_demographic_error()
swyftin.show_response_error()







#Andi Interview Simulation
AI_music_survey=survey.Survey()
AI_music_survey.add_multiple_choice_question('Please state your age range:',['18-25','26-35','36-45','46-55','55+'])
AI_music_survey.add_multiple_choice_question('Please state your gender', ['Male','Female','Prefer not to say'])
AI_music_survey.add_multiple_choice_question('What lifestyle describes your situation best?',['Rural','Urban','Suburban'])
AI_music_survey.add_multiple_choice_question('What describes you best?',['I listen to music and also produce music myself','I listen to music'])
AI_music_survey.add_linear_scale_question('How important is music to you?',0,6)
AI_music_survey.add_multiple_choice_question('On average, approximately how much time do you spend listening to music each day?',['Less than 30min','30min to 1h','More than 1h'])
AI_music_survey.add_linear_scale_question('How important is melody to you in music?',1,5)
AI_music_survey.add_linear_scale_question('How important is overall mood to you in music?',1,5)
AI_music_survey.add_linear_scale_question('How important are vocals to you in music?',1,5)
AI_music_survey.add_linear_scale_question('How important are lyrics to you in music?',1,5)
AI_music_survey.add_linear_scale_question('How important is the artist to you in music?',1,5)
AI_music_survey.add_multiple_choice_question('Do you know what generative AI is?',['Yes','No'])
AI_music_survey.add_multiple_choice_question('Are you concerned about Artificial Intelligence challenging human artistry, for example in music creation?',['Yes','No.','No Opinion'])
AI_music_survey.add_multiple_choice_question('Have you ever listened to music that has been generated via Artificial Intelligence?',['Yes','No'])
AI_music_survey.add_checkboxes_question('What features of generative music AI are the most interesting to you? (Select all that apply)',['It can create personalised songs that are customised to match your mood. As a result, these songs are uniquely composed for you.','Generative AI can combine different genres and artists to produce unique and original musical compositions.','Generative AI is able to create songs from genres that you like.','It can create new songs from specific artists that you like.'])
AI_music_survey.add_checkboxes_question('Please choose the following statements based on your perception of their importance. (Select all that apply)',['Artists should be compensated for AI= generated music that utilises their previously released music for training purposes.','AI-generated music should be clearly distinguished or highlighted for the listeners.','Artists should have complete control over the release of AI-generated music that is created using their previously released music as training data.','AI-generated music can be released without artist consent, as long as the artist gets compensated for it.'])
AI_music_survey.add_checkboxes_question('Please check all the boxes that correspond to terms you are familiar with.',['Web3 in general','NFTs','Blockchain','Crypto-currency','FIAT-currency','AI','None of the above'])
AI_music_survey.add_multiple_choice_question('Do you know what non-fungible tokens (NFTs) are?',['Yes','No'])
AI_music_survey.add_checkboxes_question('What features of non-fungible tokens (NFTs) are the most interesting to you? (Select all that apply)',['Proving ownership of digital items','Proving uniqueness of digital items','Proving scarcity of digital items','The option to re-sell your digital items and make financial gain','Smart features like royalty sharing'])

AI_music=simulation.Simulation(AI_music_survey,"AI_music")
AI_music.demographic_parameters(age='18-65',country_of_residence='Western countries')

start_time = time.time() ##16:40
AI_music.simulate(n_of_runs=70)
end_time = time.time()

AI_music.show_demographic_error()
AI_music.show_response_error()
AI_music.show_raw_demographics()
AI_music.show_raw_responses()

AI_music.show_performance()
print(str(end_time-start_time))






###Osman Simulation
invictus_survey=survey.Survey()
invictus_survey.add_long_answer_question('What is the timescale and cost of MEP and HVAC installation jobs within buildings?')
invictus_survey.add_long_answer_question('In your experience, what are the factors negatively effecting the MEP and HVAC installation jobs within buildings?')
invictus_survey.add_long_answer_question('What specific technologies or tools do you utilize to enhance productivity and address these factors?')
invictus_survey.add_long_answer_question('Could you describe a recent project where you encountered significant physical challenges to do with these jobs?')
invictus_survey.add_long_answer_question('How open are you (or your organisation) to adopting new innovations and technology in your work? If so Have you adopted/implemented any?')

invictus=simulation.Simulation(invictus_survey,"Invictus")
invictus.demographic_parameters(country_of_residence='United Kingdom and Europe',employment_status='Full-time', occupation=['construction builder','construction project manager','construction project consultant','building services engineer'])


start_time = time.time() ##15:28
invictus.simulate(n_of_runs=20)
end_time = time.time()


print(f'Runtime:' +str(end_time-start_time))

invictus.show_performance()
invictus.show_raw_demographics()
invictus.show_raw_responses()
invictus.show_demographic_error()
invictus.show_response_error()



#nikhil sim 2
nikhil_2=survey.Survey()
nikhil_2.add_multiple_choice_question('You are staying at a 3 star hotel and need assistance. The hotel uses an online guest management system to handle enquiries, with the option of contacting AI or human concierge. The current waiting time for human concierge is 1 minute, would you choose the AI concierge for help?', ['Yes', 'No'])
nikhil_2.add_multiple_choice_question('You are staying at a 3 star hotel and need assistance. The hotel uses an online guest management system to handle enquiries, with the option of contacting AI or human concierge. The current waiting time for human concierge is 2 minutes, would you choose the AI concierge for help?', ['Yes', 'No'])
nikhil_2.add_multiple_choice_question('You are staying at a 3 star hotel and need assistance. The hotel uses an online guest management system to handle enquiries, with the option of contacting AI or human concierge. The current waiting time for human concierge is 3 minutes, would you choose the AI concierge for help?', ['Yes', 'No'])
nikhil_2.add_multiple_choice_question('You are staying at a 3 star hotel and need assistance. The hotel uses an online guest management system to handle enquiries, with the option of contacting AI or human concierge. The current waiting time for human concierge is 5+ minute, would you choose the AI concierge for help?', ['Yes', 'No'])

nikhil_2_sim=simulation.Simulation(nikhil_2,"AI_chatbot")
nikhil_2_sim.demographic_parameters(age='24-40',country_of_residence='India',nationality='Indian',ethnicity='Indian',employment_status=['Full-time','Part-time'])

start_time=time.time()
nikhil_2_sim.simulate(n_of_runs=100)
end_time=time.time()


print(f'Runtime:' +str(end_time-start_time))
nikhil_2_sim.show_performance()
nikhil_2_sim.show_raw_demographics()
nikhil_2_sim.show_raw_responses()
nikhil_2_sim.show_demographic_error()
nikhil_2_sim.show_response_error()
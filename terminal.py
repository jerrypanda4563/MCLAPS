import main
import time



main.create_survey("MaMa_2")
main.post_multiple_choice_question('Please select your age range',['60-64','65-70','71-74','75-80','81-84','85 and above'])
main.post_multiple_choice_question('Please select your gender',['Male','Female','Prefer not to say','Other:'])
main.post_multiple_choice_question('If you are in London, please select your borough in London',['Barking and Dagenham','Barnet','Bexley','Brent','Bromley','Camden','City of London','Corydon','Ealing','Enfield','Greenwich','Hackney','Hammersmith and Fulham','Haringey','Harrow','Havering','Hillingdon','Hounslow','Islington','Kensington and Chelsea','Kingston upon Thames','Lambeth','Lewisham','Merton','Newham','Redbridge','Richmond upon Thames','Southwark','Sutton','Tower Hamlets','Waltham Forest','Wandsworth','Westminster','Other:'])
main.post_multiple_choice_question('Please select your current living situation',['Living alone','Living with spouse/partner','Living with family','Living in a care home','Other:'])
main.post_multiple_choice_question('Are you currently using any kind of elder care services?',['Yes','No'])
main.post_short_answer_question('If you are using elder care services, what provider and services are you using?')
main.post_linear_scale_question('How would you rate your overall quality of life in retirement?',1,7)
main.post_checkboxes_question('Which of the following challenges do you regularly face? (Select all that applies)',['Mobility issues','Access to healthcare','Loneliness','Financial difficulties','Lack of assistance with daily tasks','Other:'])
main.post_linear_scale_question('On a scale of 1-7, how would you rate your current level of social interaction and community involvement?',1,7)
main.post_checkboxes_question('What are your primary unmet needs?',['Healthcare','Companionship','Assistance with daily tasks','Financial Support','Other:'])
main.post_multiple_choice_question('Would you be open to receiving care or assistance from university students?',['Yes','No','Maybe'])
main.post_checkboxes_question('What tasks would you feel comfortable letting a university student assist you with?',['Grocery shopping','House cleaning','Medical appointments','social outings','technology tutoring','Other:'])
main.post_linear_scale_question('On a scale of 1-7, how concerned are you about interacting with university students in a caregiving context?',1,7)
main.post_multiple_choice_question('How would you prefer to connect with potential student caregivers?',['Online platform','Phone','In-person meetings','Other:'])
main.post_checkboxes_question('What qualities would you want student caregivers to have? (Select all that apply)',['Patience','Experience with elder care','Good communication skills','Reliability','Other:'])
main.post_long_answer_question('Please share any other thoughts or concerns you have about the idea of an intergenerational elder care platform.')
main.post_demographics(age="70-90",country_of_residence="United Kingdom")



start_time=time.time()
main.get_simulation_data(30)
end_time=time.time()
runtime=end_time-start_time
print(runtime)
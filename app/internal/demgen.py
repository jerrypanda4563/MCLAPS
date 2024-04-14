import openai
import json
from typing import Dict, Literal, Optional, List
from pydantic import BaseModel
from app.internal.tokenizer import count_tokens
from app.internal.mclapsrl import mclapsrlClient
from app import settings

import time
from concurrent.futures import ThreadPoolExecutor
import openai.error
import time
from threading import Lock


openai.api_key = settings.OPEN_AI_KEY
rate_limiter = mclapsrlClient()








# class DemographicModel(BaseModel):
#     sex_at_birth: Optional[Literal["Male", "Female", "Intersex"]]
#     gender_identity: Optional[Literal["Male", "Female", "Male to Female Transgender", "Female to Male Transgender", "Non-Binary"]]
#     age: int
#     marital_status: Optional[Literal["Married", "Divorced", "Widowed", "Unmarried"]]
#     sexual_orientation: Optional[Literal["Heterosexual", "Gay", "Lesbian", "Bisexual", "Pansexual", "Queer"]]
#     nationality: Optional[Literal["Afghan", "Albanian", "Algerian", "American", "Andorran", "Angolan", "Anguillan", "Citizen of Antigua and Barbuda", "Argentine", "Armenian", "Australian", "Austrian", "Azerbaijani", "Bahamian", "Bahraini", "Bangladeshi", "Barbadian", "Belarusian", "Belgian", "Belizean", "Beninese", "Bermudian", "Bhutanese", "Bolivian", "Citizen of Bosnia and Herzegovina", "Botswanan", "Brazilian", "British", "British Virgin Islander", "Bruneian", "Bulgarian", "Burkinan", "Burmese", "Burundian", "Cambodian", "Cameroonian", "Canadian", "Cape Verdean", "Cayman Islander", "Central African", "Chadian", "Chilean", "Chinese", "Colombian", "Comoran", "Congolese (Congo)", "Congolese (DRC)", "Cook Islander", "Costa Rican", "Croatian", "Cuban", "Cymraes", "Cymro", "Cypriot", "Czech", "Danish", "Djiboutian", "Dominican", "Citizen of the Dominican Republic", "Dutch", "East Timorese", "Ecuadorean", "Egyptian", "Emirati", "English", "Equatorial Guinean", "Eritrean", "Estonian", "Ethiopian", "Faroese", "Fijian", "Filipino", "Finnish", "French", "Gabonese", "Gambian", "Georgian", "German", "Ghanaian", "Gibraltarian", "Greek", "Greenlandic", "Grenadian", "Guamanian", "Guatemalan", "Citizen of Guinea-Bissau", "Guinean", "Guyanese", "Haitian", "Honduran", "Hong Konger", "Hungarian", "Icelandic", "Indian", "Indonesian", "Iranian", "Iraqi", "Irish", "Israeli", "Italian", "Ivorian", "Jamaican", "Japanese", "Jordanian", "Kazakh", "Kenyan", "Kittitian", "Citizen of Kiribati", "Kosovan", "Kuwaiti", "Kyrgyz", "Lao", "Latvian", "Lebanese", "Liberian", "Libyan", "Liechtenstein Citizen", "Lithuanian", "Luxembourger", "Macanese", "Macedonian", "Malagasy", "Malawian", "Malaysian", "Maldivian", "Malian", "Maltese", "Marshallese", "Martiniquais", "Mauritanian", "Mauritian", "Mexican", "Micronesian", "Moldovan", "Monegasque", "Mongolian", "Montenegrin", "Montserratian", "Moroccan", "Mosotho", "Mozambican", "Namibian", "Nauruan", "Nepalese", "New Zealander", "Nicaraguan", "Nigerian", "Nigerien", "Niuean", "North Korean", "Northern Irish", "Norwegian", "Omani", "Pakistani", "Palauan", "Palestinian", "Panamanian", "Papua New Guinean", "Paraguayan", "Peruvian", "Pitcairn Islander", "Polish", "Portuguese", "Prydeinig", "Puerto Rican", "Qatari", "Romanian", "Russian", "Rwandan", "Salvadorean", "Sammarinese", "Samoan", "Sao Tomean", "Saudi Arabian", "Scottish", "Senegalese", "Serbian", "Citizen of Seychelles", "Sierra Leonean", "Singaporean", "Slovak", "Slovenian", "Solomon Islander", "Somali", "South African", "South Korean", "South Sudanese", "Spanish", "Sri Lankan", "St Helenian", "St Lucian", "Stateless", "Sudanese", "Surinamese", "Swazi", "Swedish", "Swiss", "Syrian", "Taiwanese", "Tajik", "Tanzanian", "Thai", "Togolese", "Tongan", "Trinidadian", "Tristanian", "Tunisian", "Turkish", "Turkmen", "Turks and Caicos Islander", "Tuvaluan", "Ugandan", "Ukrainian", "Uruguayan", "Uzbek", "Vatican citizen", "Citizen of Vanuatu", "Venezuelan", "Vietnamese", "Vincentian", "Wallisian", "Welsh", "Yemeni", "Zambian", "Zimbabwean"]]
#     country_of_residence: Optional[Literal["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Anguilla", "Antarctica/British Antarctic Territory", "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bonaire/St Eustatius/Saba", "Bosnia and Herzegovina", "Botswana", "Brazil", "British Indian Ocean Territory", "British Virgin Islands", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Cook Islands, Tokelau and Niue", "Costa Rica", "Côte d'Ivoire", "Croatia", "Cuba", "Curaçao", "Cyprus", "Czech Republic", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Falkland Islands", "Fiji", "Finland", "France", "French Guiana", "French Polynesia", "Gabon", "The Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Grenada", "Guadeloupe", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macao", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Montserrat", "Morocco", "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "The Occupied Palestinian Territories", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcairn Island", "Poland", "Portugal", "Qatar", "Réunion", "Romania", "Russia", "Rwanda", "Samoa", "San Marino", "São Tomé and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Georgia and the South Sandwich Islands", "South Korea", "South Sudan", "Spain", "Sri Lanka", "St Helena, Ascension and Tristan da Cunha", "St Kitts and Nevis", "St Lucia", "St Maarten", "St Martin and St Barthélemy", "St Pierre & Miquelon", "St Vincent and the Grenadines", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu", "USA", "Uganda", "Ukraine", "United Arab Emirates", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Wallis and Futuna", "Western Sahara", "Yemen", "Zambia", "Zimbabwe"]]
#     state_province:str
#     city: str
#     rural_or_urban: Optional[Literal["Rural", "Urban", "Suburban"]]
#     type_of_residence: Optional[Literal["Apartment/Flat", "Detached house", "Semi-detached house", "Terraced house", "End of terraced house", "Bungalow", "Farm", "Mansion"]]
#     length_of_residence: int
#     level_of_education: Optional[Literal["Primary or under", "Lower secondary", "Upper secondary", "Bachelor", "Master", "PhD", "Post Doctorate"]]
#     student_status: Optional[Literal["Full-time", "Part-time", "Non-student"]]
#     field_of_study: Optional[Literal["Natural Sciences", "Engineering & Technology", "Medical Sciences & Health", "Social Sciences", "Humanities", "Arts & Design", "Business & Economics", "Law & Legal Studies", "Mathematics & Statistics", "Education", "Agricultural & Environmental Sciences", "Interdisciplinary Studies", "Other"]]
#     occupational_area: Optional[Literal["Agriculture & Forestry", "Arts, Design, Entertainment, Sports, and Media", "Business & Finance", "Education & Teaching", "Engineering & Architecture", "Healthcare & Medical Professions", "Hospitality & Tourism", "Information Technology & Computer Sciences", "Legal Professions", "Manufacturing & Production", "Media & Communications", "Personal Care & Services", "Public Service & Government", "Real Estate", "Retail & Customer Service", "Science & Research", "Senior Management & Business Owners", "Entrepreneurs", "Social Services & Non-Profit", "Trades & Construction", "Transportation & Logistics", "Other"]]
#     annual_income_level: int 
#     employment_status: Optional[Literal["Full-time", "Part-time", "Unemployed", "Self-employed/Freelance", "Business Owner/Entrepreneur"]]
#     home_ownership: Optional[Literal["Mortgaged", "Fully Owned", "Renting"]]
#     ethnicity: Optional[Literal["East Asian", "Southeast Asian", "South Asian", "Central Asian", "North African", "Sub-Saharan African", "Western European", "Northern European", "Southern European", "Eastern European", "Arab", "Persian", "Turkish", "Israeli", "Central American", "South American", "Caribbean", "Polynesian", "Micronesian", "Melanesian", "Native American", "Aboriginal Australian", "Multi-ethnic", "Other"]]
#     languages_spoken: Optional[Literal["Amharic", "Arabic", "Armenian", "Basque", "Bengali", "Bulgarian", "Burmese", "Cantonese", "Czech", "Danish", "Dutch", "English", "Estonian", "Farsi", "Filipino", "Finnish", "French", "Georgian", "German", "Greek", "Guarani", "Gujarati", "Hausa", "Hawaiian", "Hebrew", "Hindi", "Hungarian", "Igbo", "Indonesian", "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Korean", "Kurdish", "Latin", "Malay", "Malayalam", "Maori", "Marathi", "Mandarin", "Norwegian", "Oromo", "Pashto", "Polish", "Portuguese", "Punjabi", "Quechua", "Romanian", "Russian", "Serbian", "Shanghainese", "Somali", "Spanish", "Swahili", "Swedish", "Tagalog", "Tahitian", "Tamil", "Telugu", "Thai", "Tibetan", "Turkish", "Turkmen", "Ukrainian", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yoruba", "Zulu", "Other"]]
#     religion: Optional[Literal["Buddhism", "Christianity", "Confucianism", "Hinduism", "Islam", "Jainism", "Judaism", "Shinto", "Sikhism", "Taoism", "Zoroastrianism", "Other"]]
#     cultural_practices: Optional[Literal["No Engagement", "Minimal Awareness", "Occasional Participation", "Selective Adoption", "Moderate Engagement", "Bicultural", "Consistent Participation", "Cultural Advocate", "Cultural Preservationist", "Total Immersion"]]
#     immigration_status: Optional[Literal["Natural-Born Citizen", "Naturalized Citizen", "Permanent Resident", "Temporary Resident", "Refugee or Asylee", "Undocumented Immigrant", "Diplomatic Status", "Humanitarian or Protected Status", "Conditional Resident", "Stateless Person"]]
#     hobbies_and_interests: Optional[Literal["Acting", "Animal welfare", "Antiques", "Astronomy", "Attending theater, opera, ballet", "Backpacking", "Birdwatching", "Blogging", "Board games", "Bonsai and gardening", "Building computers", "Stand-up comedy", "Fishing", "Journaling", "Electronics DIY", "Bread making", "Cake decorating", "Camping", "Kayaking", "Coding", "Community service", "Creative writing", "Poetry", "Cultural immersion", "Dance", "DIY projects", "Woodworking", "Traveling/Tourism", "Drawing", "Sculpting", "Embroidery", "Environmental activism", "Cooking", "Figurines", "Gym", "Yoga", "Pilates", "Historical site exploration", "History", "Horticulture", "Knitting and sewing", "Landscaping", "Language learning", "Memorabilia", "Museums and galleries", "Music instruments", "Attending online courses and workshops", "Painting", "Photography", "Reading", "Robotics", "Rock climbing", "Running", "Screenwriting", "Storytelling", "Singing", "Stamps and coin collecting", "Competitive Team Sports", "Cycling", "Video gaming", "Visiting museums and galleries", "Volunteering and Social Service", "Wine and beer brewing", "Other"]]
#     shopping_motivations: Optional[Literal["Convenience", "Price", "Quality", "Trend", "Need", "Ethics", "Brand"]]
#     shopping_habits: Optional[Literal["Pre-planned shopper", "Exploratory shopper", "Habitual shopper", "Seasonal shopper", "Bulk shopper", "Efficiency shopper", "Social shopper", "Bargain shopper", "Research-intensive shopper"]]
#     shopping_channels: Optional[Literal["Online", "In-Store", "Online and Offline"]]
#     shopping_frequency: int
#     dietary_preferences: Optional[Literal["Vegetarian", "Vegan", "Pescatarian", "Ketogenic", "Gluten-free", "Lactose-free", "Halal", "Kosher", "Omnivorous"]]
#     physical_activity_levels: Optional[Literal["Not physically active", "Lightly active", "Moderately active", "Highly active", "Extremely active"]]
#     social_media_usage: Optional[Literal["Not active on social media", "Light social media user", "Moderate social media user", "Heavy social media user", "Social media addict"]]
#     travel_habits: Optional[Literal["Seasonal vacationer", "Weekend traveller", "Business traveller", "Luxury traveller", "Budget traveller", "Eco-tourist", "Solo traveller", "Group traveller"]]
#     alcohol_use: Optional[Literal["Does not drink alcohol", "Social drinker", "Daily drinker", "Heavy drinker", "Alcoholic"]]
#     tobacco_and_vape_use: Optional[Literal["Does not smoke", "Social smoker", "Daily smoker", "Heavy smoker", "Nicotine addict"]]
#     technology_usage: Optional[Literal["Non-Users", "Occasional Users", "Routine Users", "Confident Users", "Advanced Users", "Tech Enthusiasts", "Professional Users", "Digital Creators", "Innovators and Developers"]]
#     family_structure: Optional[Literal["Nuclear Family", "Single-Parent Family", "Extended Family", "Childless Family", "Stepfamily", "Grandparent Family", "Same-Sex Family", "Communal Family", "Foster Family", "Dual-Income Family", "Single Person Household", "Co-Parenting Family"]]
#     household_size: int
#     number_of_children: int
#     pet_ownership: Optional[Literal["Does not own pets", "Dogs", "Cats", "Aquarius Animals", "Bird Animals", "Small Mammals", "Reptile", "Amphibians", "Insects", "Arachnids", "Large Animals"]]
#     number_of_pets: int
#     relationship_status: Optional[Literal["Single", "Dating", "Engaged", "Married", "Cohabiting", "Domestic Partnership", "Separated", "Divorced", "Widowed", "Civil Union", "Complicated", "Open Relationship"]]
#     caregiving_responsibilities: Optional[Literal["Child Care", "Elderly Care", "Special Needs Care", "Household Care", "End-of-Life Care", "Pet Care", "Community Care"]]
#     general_health_status: Optional[Literal["Fully healthy", "Minor health issues", "Major health issues", "Improving health status", "Declining health status", "Partially disabled"]]
#     disabilities_or_chronic_illnesses: Optional[Literal["None", "Physical Disabilities", "Sensory Impairments", "Chronic Pain Disorders", "Respiratory Disorders", "Cardiovascular Diseases", "Neurological Disorders", "Mental Health Disorders", "Gastrointestinal Disorders", "Endocrine Disorders", "Autoimmune Diseases", "Blood Disorders", "Renal and Urological Disorders", "Cancer", "Infectious Diseases", "Developmental Disorders"]]
#     mental_health_status: Optional[Literal["Optimal Mental Health", "Good Mental Health", "Mild Mental Health Issues", "Moderate Mental Health Issues", "Poor Mental Health", "Severe Mental Health Disorders", "In Crisis or Acute Distress", "Recovering or Improving", "Unstable Mental Health", "Stable Under Treatment"]]
#     health_insurance_status: Optional[Literal["Fully Insured (Private)", "Public Health Insurance", "Employer-Provided Insurance", "Underinsured", "Uninsured", "Gap Insurance"]]
#     access_to_healthcare: Optional[Literal["Full Access", "Limited Access", "Emergency-Only Access", "Inconsistent Access", "Low Access", "No Direct Access", "Virtual/Telehealth Access", "Financially Restricted Access"]]
#     political_affiliation: Optional[Literal["Left-winged", "Extreme left-winged", "Right-winged", "Extreme right-winged", "Politically neutral"]]
#     voting_behavior: Optional[Literal["Does not vote", "Unable to vote", "Votes in major election", "Votes in major and minor elections"]]
#     political_engagement: Optional[Literal["Not engaged", "Mildly engaged", "Moderately engaged", "Highly engaged", "Extremely engaged"]]



response_schema = {
        "Sex at Birth": "str",
        "Gender Identity": "str",
        "Age": "int",
        "Marital Status": "str",
        "Sexual Orientation": "str",
        "Nationality": "str",
        "Country of Residence": "str",
        "State/Province": "str",
        "City": "str",
        "Rural or Urban": "str",
        "Type of Residence": "str",
        "Length of Residence": "str",
        "Level of Education": "str",
        "Student Status": "str",
        "Field of Study": "str",
        "Occupational Area": "str",
        "Annual Income Level": "int",
        "Employment Status": "str",
        "Home Ownership": "str",
        "Ethnicity": "str",
        "Language(s) Spoken": "str",
        "Religion": "str",
        "Cultural Practices": "str",
        "Immigration Status": "str",
        "Hobbies and Interests": "str",
        "Shopping Motivations": "str",
        "Shopping Habits": "str",
        "Shopping Channels": "str",
        "Shopping Frequency": "str",
        "Dietary Preferences": "str",
        "Physical Activity Levels": "str",
        "Social Media Usage": "str",
        "Travel Habits": "str",
        "Alcohol Use": "str",
        "Tobacco and Vape Use": "str",
        "Technology Usage": "str",
        "Family Structure": "str",
        "Household Size": "str",
        "Number of Children": "int",
        "Pet Ownership": "str",
        "Number of Pets": "str",
        "Relationship Status": "str",
        "Caregiving Responsibilities": "str",
        "General Health Status": "str",
        "Disabilities or Chronic Illnesses": "str",
        "Mental Health Status": "str",
        "Health Insurance Status": "str",
        "Access to Healthcare": "str",
        "Political Affiliation": "str",
        "Voting Behavior": "str",
        "Political Engagement": "str"
        }

#add limiter
def generate_demographic(demo: Dict, response_model: Optional[str] = "gpt-3.5-turbo"):
    prompt_data = {
        "Sex at Birth": demo["sex_at_birth"],
        "Gender Identity": demo["gender_identity"],
        "Age": demo["age"],
        "Marital Status": demo["marital_status"],
        "Sexual Orientation": demo["sexual_orientation"],
        "Nationality": demo["nationality"],
        "Country of Residence": demo["country_of_residence"],
        "State/Province": demo["state_province"],
        "City": demo["city"],
        "Rural or Urban": demo["rural_or_urban"],
        "Type of Residence": demo["type_of_residence"],
        "Length of Residence": demo["length_of_residence"],
        "Level of Education": demo["level_of_education"],
        "Student Status": demo["student_status"],
        "Field of Study": demo["field_of_study"],
        "Occupational Area": demo["occupational_area"],
        "Annual Income Level": demo["annual_income_level"],
        "Employment Status": demo["employment_status"],
        "Home Ownership": demo["home_ownership"],
        "Ethnicity": demo["ethnicity"],
        "Language(s) Spoken": demo["languages_spoken"],
        "Religion": demo["religion"],
        "Cultural Practices": demo["cultural_practices"],
        "Immigration Status": demo["immigration_status"],
        "Hobbies and Interests": demo["hobbies_and_interests"],
        "Shopping Motivations": demo["shopping_motivations"],
        "Shopping Habits": demo["shopping_habits"],
        "Shopping Channels": demo["shopping_channels"],
        "Shopping Frequency": demo["shopping_frequency"],
        "Dietary Preferences": demo["dietary_preferences"],
        "Physical Activity Levels": demo["physical_activity_levels"],
        "Social Media Usage": demo["social_media_usage"],
        "Travel Habits": demo["travel_habits"],
        "Alcohol Use": demo["alcohol_use"],
        "Tobacco and Vape Use": demo["tobacco_and_vape_use"],
        "Technology Usage": demo["technology_usage"],
        "Family Structure": demo["family_structure"],
        "Household Size": demo["household_size"],
        "Number of Children": demo["number_of_children"],
        "Pet Ownership": demo["pet_ownership"],
        "Number of Pets": demo["number_of_pets"],
        "Relationship Status": demo["relationship_status"],
        "Caregiving Responsibilities": demo["caregiving_responsibilities"],
        "General Health Status": demo["general_health_status"],
        "Disabilities or Chronic Illnesses": demo["disabilities_or_chronic_illnesses"],
        "Mental Health Status": demo["mental_health_status"],
        "Health Insurance Status": demo["health_insurance_status"],
        "Access to Healthcare": demo["access_to_healthcare"],
        "Political Affiliation": demo["political_affiliation"],
        "Voting Behavior": demo["voting_behavior"],
        "Political Engagement": demo["political_engagement"]
    }
    schema = json.dumps(response_schema)
    
    system_prompt = json.dumps({k: v for k, v in prompt_data.items() if v is not None})
    prompt = "General demographic group:\n" + system_prompt + "\nJSON Response schema:\n"+schema

    while rate_limiter.model_status(response_model) == False:
        time.sleep(2)
    response = openai.ChatCompletion.create(
        model=response_model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system",
            "content": "Create a demographic profile of an individual belonging to a general demographic group. You must follow the JSON response schema provided."},
            {"role": "user",
            "content": prompt}
        ],
        temperature=1.3,
        max_tokens=round(2*count_tokens(schema)),
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    rate_limiter.new_response(response.dict())
    demographic_profile = response.choices[0].message.content
    return demographic_profile
            
        




class Demographic_Generator():
    def __init__(self, demo: Dict, n_of_results: int):
        self.demo = demo
        self.n_of_results = n_of_results
        self.demographic_data: List[Dict] = []
        self.schema: Dict = response_schema
        self.n_of_errors: int = 0
        self.wait_lock=Lock()
        self.should_wait = False
    
    def response_validator(self, demo_profile: str) -> bool: 
        if demo_profile is None:
            return False
        else:
            try:
                profile_dict = json.loads(demo_profile)
            except Exception as e:
                print(f"JSON string formatting incorrect: {e}")
                self.n_of_errors += 1
                return False
            
            if set(profile_dict.keys()) != set(self.schema.keys()):
                print(f"Incorrect response schema.")
                self.n_of_errors += 1
                return False
            
            return True
        
        
    def generate_profile(self) -> Dict:
        demo = None  # Initialize demo to an invalid value
        while not self.response_validator(demo):
            try:
                demo = generate_demographic(self.demo)
            except (openai.error.ServiceUnavailableError, openai.error.Timeout, openai.error.RateLimitError) as e:
                print(f'OpenAI error {e}')
                with self.wait_lock:  # Flag all threads to wait on encountering an error
                    self.should_wait = True
                wait_time=60
                print (f'Waiting for {wait_time} seconds before resuming.')
                time.sleep(wait_time)
            except Exception as e:
                print(f"An error occurred while generating demographic profile: {e}")
        demo_data = json.loads(demo)
        return demo_data
        
    
    def generate_demographic_dataset(self) -> List[Dict]:
        if self.n_of_results < 100:
            num_workers = self.n_of_results
        else:
            num_workers = 100
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_to_profile = {executor.submit(self.generate_profile): _ for _ in range(self.n_of_results)}
            for future in future_to_profile:
                profile = future.result()
                self.demographic_data.append(profile)
                n_of_profiles_generated = len(self.demographic_data)
                print(f"Generated {n_of_profiles_generated} of {self.n_of_results} profiles. Number of errors: {self.n_of_errors}.")
        return self.demographic_data

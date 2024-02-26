import openai
import json
from typing import Dict, Literal, Optional, List
from pydantic import BaseModel


import os
from app import settings

openai.api_key = settings.OPEN_AI_KEY







# class DemographicModel(BaseModel):
#     sex_at_birth: Literal["Male", "Female", "Intersex"]
#     gender_identity: Literal["Male", "Female", "Male to Female Transgender", "Female to Male Transgender", "Non-Binary"]
#     age: int
#     marital_status: Literal["Married", "Divorced", "Widowed", "Unmarried"]
#     sexual_orientation: Literal["Heterosexual", "Gay", "Lesbian", "Bisexual", "Pansexual", "Queer"]
#     nationality: Literal["Afghan", "Albanian", "Algerian", "American", "Andorran", "Angolan", "Anguillan", "Citizen of Antigua and Barbuda", "Argentine", "Armenian", "Australian", "Austrian", "Azerbaijani", "Bahamian", "Bahraini", "Bangladeshi", "Barbadian", "Belarusian", "Belgian", "Belizean", "Beninese", "Bermudian", "Bhutanese", "Bolivian", "Citizen of Bosnia and Herzegovina", "Botswanan", "Brazilian", "British", "British Virgin Islander", "Bruneian", "Bulgarian", "Burkinan", "Burmese", "Burundian", "Cambodian", "Cameroonian", "Canadian", "Cape Verdean", "Cayman Islander", "Central African", "Chadian", "Chilean", "Chinese", "Colombian", "Comoran", "Congolese (Congo)", "Congolese (DRC)", "Cook Islander", "Costa Rican", "Croatian", "Cuban", "Cymraes", "Cymro", "Cypriot", "Czech", "Danish", "Djiboutian", "Dominican", "Citizen of the Dominican Republic", "Dutch", "East Timorese", "Ecuadorean", "Egyptian", "Emirati", "English", "Equatorial Guinean", "Eritrean", "Estonian", "Ethiopian", "Faroese", "Fijian", "Filipino", "Finnish", "French", "Gabonese", "Gambian", "Georgian", "German", "Ghanaian", "Gibraltarian", "Greek", "Greenlandic", "Grenadian", "Guamanian", "Guatemalan", "Citizen of Guinea-Bissau", "Guinean", "Guyanese", "Haitian", "Honduran", "Hong Konger", "Hungarian", "Icelandic", "Indian", "Indonesian", "Iranian", "Iraqi", "Irish", "Israeli", "Italian", "Ivorian", "Jamaican", "Japanese", "Jordanian", "Kazakh", "Kenyan", "Kittitian", "Citizen of Kiribati", "Kosovan", "Kuwaiti", "Kyrgyz", "Lao", "Latvian", "Lebanese", "Liberian", "Libyan", "Liechtenstein Citizen", "Lithuanian", "Luxembourger", "Macanese", "Macedonian", "Malagasy", "Malawian", "Malaysian", "Maldivian", "Malian", "Maltese", "Marshallese", "Martiniquais", "Mauritanian", "Mauritian", "Mexican", "Micronesian", "Moldovan", "Monegasque", "Mongolian", "Montenegrin", "Montserratian", "Moroccan", "Mosotho", "Mozambican", "Namibian", "Nauruan", "Nepalese", "New Zealander", "Nicaraguan", "Nigerian", "Nigerien", "Niuean", "North Korean", "Northern Irish", "Norwegian", "Omani", "Pakistani", "Palauan", "Palestinian", "Panamanian", "Papua New Guinean", "Paraguayan", "Peruvian", "Pitcairn Islander", "Polish", "Portuguese", "Prydeinig", "Puerto Rican", "Qatari", "Romanian", "Russian", "Rwandan", "Salvadorean", "Sammarinese", "Samoan", "Sao Tomean", "Saudi Arabian", "Scottish", "Senegalese", "Serbian", "Citizen of Seychelles", "Sierra Leonean", "Singaporean", "Slovak", "Slovenian", "Solomon Islander", "Somali", "South African", "South Korean", "South Sudanese", "Spanish", "Sri Lankan", "St Helenian", "St Lucian", "Stateless", "Sudanese", "Surinamese", "Swazi", "Swedish", "Swiss", "Syrian", "Taiwanese", "Tajik", "Tanzanian", "Thai", "Togolese", "Tongan", "Trinidadian", "Tristanian", "Tunisian", "Turkish", "Turkmen", "Turks and Caicos Islander", "Tuvaluan", "Ugandan", "Ukrainian", "Uruguayan", "Uzbek", "Vatican citizen", "Citizen of Vanuatu", "Venezuelan", "Vietnamese", "Vincentian", "Wallisian", "Welsh", "Yemeni", "Zambian", "Zimbabwean"]
#     country_of_residence: Literal["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Anguilla", "Antarctica/British Antarctic Territory", "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bonaire/St Eustatius/Saba", "Bosnia and Herzegovina", "Botswana", "Brazil", "British Indian Ocean Territory", "British Virgin Islands", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Cook Islands, Tokelau and Niue", "Costa Rica", "Côte d'Ivoire", "Croatia", "Cuba", "Curaçao", "Cyprus", "Czech Republic", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Falkland Islands", "Fiji", "Finland", "France", "French Guiana", "French Polynesia", "Gabon", "The Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Grenada", "Guadeloupe", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macao", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Montserrat", "Morocco", "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "The Occupied Palestinian Territories", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Pitcairn Island", "Poland", "Portugal", "Qatar", "Réunion", "Romania", "Russia", "Rwanda", "Samoa", "San Marino", "São Tomé and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Georgia and the South Sandwich Islands", "South Korea", "South Sudan", "Spain", "Sri Lanka", "St Helena, Ascension and Tristan da Cunha", "St Kitts and Nevis", "St Lucia", "St Maarten", "St Martin and St Barthélemy", "St Pierre & Miquelon", "St Vincent and the Grenadines", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands", "Tuvalu", "USA", "Uganda", "Ukraine", "United Arab Emirates", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Wallis and Futuna", "Western Sahara", "Yemen", "Zambia", "Zimbabwe"]
#     state_province:str
#     city: str
#     rural_or_urban: Literal["Rural", "Urban", "Suburban"]
#     type_of_residence: Literal["Apartment/Flat", "Detached house", "Semi-detached house", "Terraced house", "End of terraced house", "Bungalow", "Farm", "Mansion"]
#     length_of_residence: int
#     level_of_education: Literal["Primary or under", "Lower secondary", "Upper secondary", "Bachelor", "Master", "PhD", "Post Doctorate"]
#     student_status: Literal["Full-time", "Part-time", "Non-student"]
#     field_of_study: Literal["Natural Sciences", "Engineering & Technology", "Medical Sciences & Health", "Social Sciences", "Humanities", "Arts & Design", "Business & Economics", "Law & Legal Studies", "Mathematics & Statistics", "Education", "Agricultural & Environmental Sciences", "Interdisciplinary Studies", "Other"]
#     occupational_area: Literal["Agriculture & Forestry", "Arts, Design, Entertainment, Sports, and Media", "Business & Finance", "Education & Teaching", "Engineering & Architecture", "Healthcare & Medical Professions", "Hospitality & Tourism", "Information Technology & Computer Sciences", "Legal Professions", "Manufacturing & Production", "Media & Communications", "Personal Care & Services", "Public Service & Government", "Real Estate", "Retail & Customer Service", "Science & Research", "Senior Management & Business Owners", "Entrepreneurs", "Social Services & Non-Profit", "Trades & Construction", "Transportation & Logistics", "Other"]
#     annual_income_level: int 
#     employment_status: Literal["Full-time", "Part-time", "Unemployed", "Self-employed/Freelance", "Business Owner/Entrepreneur"]
#     home_ownership: Literal["Mortgaged", "Fully Owned", "Renting"]
#     ethnicity: Literal["East Asian", "Southeast Asian", "South Asian", "Central Asian", "North African", "Sub-Saharan African", "Western European", "Northern European", "Southern European", "Eastern European", "Arab", "Persian", "Turkish", "Israeli", "Central American", "South American", "Caribbean", "Polynesian", "Micronesian", "Melanesian", "Native American", "Aboriginal Australian", "Multi-ethnic", "Other"]
#     languages_spoken: Literal["Amharic", "Arabic", "Armenian", "Basque", "Bengali", "Bulgarian", "Burmese", "Cantonese", "Czech", "Danish", "Dutch", "English", "Estonian", "Farsi", "Filipino", "Finnish", "French", "Georgian", "German", "Greek", "Guarani", "Gujarati", "Hausa", "Hawaiian", "Hebrew", "Hindi", "Hungarian", "Igbo", "Indonesian", "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Korean", "Kurdish", "Latin", "Malay", "Malayalam", "Maori", "Marathi", "Mandarin", "Norwegian", "Oromo", "Pashto", "Polish", "Portuguese", "Punjabi", "Quechua", "Romanian", "Russian", "Serbian", "Shanghainese", "Somali", "Spanish", "Swahili", "Swedish", "Tagalog", "Tahitian", "Tamil", "Telugu", "Thai", "Tibetan", "Turkish", "Turkmen", "Ukrainian", "Uzbek", "Vietnamese", "Welsh", "Xhosa", "Yoruba", "Zulu", "Other"]
#     religion: Literal["Buddhism", "Christianity", "Confucianism", "Hinduism", "Islam", "Jainism", "Judaism", "Shinto", "Sikhism", "Taoism", "Zoroastrianism", "Other"]
#     cultural_practices: Literal["No Engagement", "Minimal Awareness", "Occasional Participation", "Selective Adoption", "Moderate Engagement", "Bicultural", "Consistent Participation", "Cultural Advocate", "Cultural Preservationist", "Total Immersion"]
#     immigration_status: Literal["Natural-Born Citizen", "Naturalized Citizen", "Permanent Resident", "Temporary Resident", "Refugee or Asylee", "Undocumented Immigrant", "Diplomatic Status", "Humanitarian or Protected Status", "Conditional Resident", "Stateless Person"]
#     hobbies_and_interests: Literal["Acting", "Animal welfare", "Antiques", "Astronomy", "Attending theater, opera, ballet", "Backpacking", "Birdwatching", "Blogging", "Board games", "Bonsai and gardening", "Building computers", "Stand-up comedy", "Fishing", "Journaling", "Electronics DIY", "Bread making", "Cake decorating", "Camping", "Kayaking", "Coding", "Community service", "Creative writing", "Poetry", "Cultural immersion", "Dance", "DIY projects", "Woodworking", "Traveling/Tourism", "Drawing", "Sculpting", "Embroidery", "Environmental activism", "Cooking", "Figurines", "Gym", "Yoga", "Pilates", "Historical site exploration", "History", "Horticulture", "Knitting and sewing", "Landscaping", "Language learning", "Memorabilia", "Museums and galleries", "Music instruments", "Attending online courses and workshops", "Painting", "Photography", "Reading", "Robotics", "Rock climbing", "Running", "Screenwriting", "Storytelling", "Singing", "Stamps and coin collecting", "Competitive Team Sports", "Cycling", "Video gaming", "Visiting museums and galleries", "Volunteering and Social Service", "Wine and beer brewing", "Other"]
#     shopping_motivations: Literal["Convenience", "Price", "Quality", "Trend", "Need", "Ethics", "Brand"]
#     shopping_habits: Literal["Pre-planned shopper", "Exploratory shopper", "Habitual shopper", "Seasonal shopper", "Bulk shopper", "Efficiency shopper", "Social shopper", "Bargain shopper", "Research-intensive shopper"]
#     shopping_channels: Literal["Online", "In-Store", "Online and Offline"]
#     shopping_frequency: int
#     dietary_preferences: Literal["Vegetarian", "Vegan", "Pescatarian", "Ketogenic", "Gluten-free", "Lactose-free", "Halal", "Kosher", "Omnivorous"]
#     physical_activity_levels: Literal["Not physically active", "Lightly active", "Moderately active", "Highly active", "Extremely active"]
#     social_media_usage: Literal["Not active on social media", "Light social media user", "Moderate social media user", "Heavy social media user", "Social media addict"]
#     travel_habits: Literal["Seasonal vacationer", "Weekend traveller", "Business traveller", "Luxury traveller", "Budget traveller", "Eco-tourist", "Solo traveller", "Group traveller"]
#     alcohol_use: Literal["Does not drink alcohol", "Social drinker", "Daily drinker", "Heavy drinker", "Alcoholic"]
#     tobacco_and_vape_use: Literal["Does not smoke", "Social smoker", "Daily smoker", "Heavy smoker", "Nicotine addict"]
#     technology_usage: Literal["Non-Users", "Occasional Users", "Routine Users", "Confident Users", "Advanced Users", "Tech Enthusiasts", "Professional Users", "Digital Creators", "Innovators and Developers"]
#     family_structure: Literal["Nuclear Family", "Single-Parent Family", "Extended Family", "Childless Family", "Stepfamily", "Grandparent Family", "Same-Sex Family", "Communal Family", "Foster Family", "Dual-Income Family", "Single Person Household", "Co-Parenting Family"]
#     household_size: int
#     number_of_children: int
#     pet_ownership: Literal["Does not own pets", "Dogs", "Cats", "Aquarius Animals", "Bird Animals", "Small Mammals", "Reptile", "Amphibians", "Insects", "Arachnids", "Large Animals"]
#     number_of_pets: int
#     relationship_status: Literal["Single", "Dating", "Engaged", "Married", "Cohabiting", "Domestic Partnership", "Separated", "Divorced", "Widowed", "Civil Union", "Complicated", "Open Relationship"]
#     caregiving_responsibilities: Literal["Child Care", "Elderly Care", "Special Needs Care", "Household Care", "End-of-Life Care", "Pet Care", "Community Care"]
#     general_health_status: Literal["Fully healthy", "Minor health issues", "Major health issues", "Improving health status", "Declining health status", "Partially disabled"]
#     disabilities_or_chronic_illnesses: Literal["None", "Physical Disabilities", "Sensory Impairments", "Chronic Pain Disorders", "Respiratory Disorders", "Cardiovascular Diseases", "Neurological Disorders", "Mental Health Disorders", "Gastrointestinal Disorders", "Endocrine Disorders", "Autoimmune Diseases", "Blood Disorders", "Renal and Urological Disorders", "Cancer", "Infectious Diseases", "Developmental Disorders"]
#     mental_health_status: Literal["Optimal Mental Health", "Good Mental Health", "Mild Mental Health Issues", "Moderate Mental Health Issues", "Poor Mental Health", "Severe Mental Health Disorders", "In Crisis or Acute Distress", "Recovering or Improving", "Unstable Mental Health", "Stable Under Treatment"]
#     health_insurance_status: Literal["Fully Insured (Private)", "Public Health Insurance", "Employer-Provided Insurance", "Underinsured", "Uninsured", "Gap Insurance"]
#     access_to_healthcare: Literal["Full Access", "Limited Access", "Emergency-Only Access", "Inconsistent Access", "Low Access", "No Direct Access", "Virtual/Telehealth Access", "Financially Restricted Access"]
#     political_affiliation: Literal["Left-winged", "Extreme left-winged", "Right-winged", "Extreme right-winged", "Politically neutral"]
#     voting_behavior: Literal["Does not vote", "Unable to vote", "Votes in major election", "Votes in major and minor elections"]
#     political_engagement: Literal["Not engaged", "Mildly engaged", "Moderately engaged", "Highly engaged", "Extremely engaged"]






def generate_demographic(demo: Dict):
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
    prompt = json.dumps({k: None for k in prompt_data.keys()})
    system_prompt = json.dumps({k: v for k, v in prompt_data.items() if v is not None})
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system",
             "content": "Create a demographic profile of an individuals in json format. The constrained parameters are:\n" + system_prompt + "\nReplace the constrained value with a value falling reasonably within the category."},
            {"role": "user",
             "content": prompt}
        ],
        temperature=1.3,
        max_tokens=1366,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    demographic_profile = response.choices[0].message.content
    return demographic_profile



from app import main
from app.internal import demgen, survey
from app.internal import simulation_runner as runner


# comment: survey specifics still require optimization, output still as default into simulation folder in csv.

# simulation 1: Pricing Research on a New Fitness Tracker
def pricing_simulation(n, v_age: str = '20-40', v_country_of_residence: str = "United Kingdom",
                       v_income_level: str = "£60000 to £80000"):
    s = survey.Survey("Pricing_2")
    s.description = "Survey for Pricing Research on a New Fitness Tracker"
    # Section 1 Demographics
    s.add_short_answer_question("Age:")
    s.add_multiple_choice_question("Gender:", ["Male", "Female", "Non-Binary"])
    s.add_short_answer_question("Occupation:")
    # Section 2 Existing behavior
    s.add_multiple_choice_question("Do you currently use a fitness tracker?", ["Yes", "No"])
    s.add_short_answer_question("If yes, which brand/model of fitness tracker do you use?")
    s.add_checkboxes_question("What features do you most value in a fitness tracker?",
                              ["Activity tracking (steps, distance, calories burned, etc.)", "Heart rate monitoring",
                               "Sleep tracking", "GPS navigation", "Smartphone notifications", "Battery life",
                               "Aesthetic/design"])
    # Section 3 pricing
    s.add_linear_scale_question(
        "At a price of $50, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
        1, 10)
    s.add_linear_scale_question(
        "At a price of $100, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
        1, 10)
    s.add_linear_scale_question(
        "At a price of $150, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
        1, 10)
    s.add_linear_scale_question(
        "At a price of $200, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
        1, 10)
    s.add_linear_scale_question(
        "At a price of $250, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
        1, 10)
    s.add_linear_scale_question(
        "At a price of $300, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
        1, 10)
    s.add_linear_scale_question(
        "At a price of $350, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
        1, 10)
    s.add_linear_scale_question(
        "At a price of $400, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
        1, 10)
    s.add_linear_scale_question(
        "At a price of $500, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
        1, 10)
    s.add_linear_scale_question(
        "At a price of $600, how likely would you be to purchase the fitness tracker? (1 being least likely and 10 being most likely)",
        1, 10)
    demo = demgen.Demographic(
        age=v_age,  # variable
        income_level=v_income_level,
        hobbies_and_interests='Interest in fitness, wellness, and technology',
        physical_activity_levels='Moderate to high',
        social_media_usage='Moderate to high',
        general_health_status='Good to excellent',
    )
    runner.get_simulation_data(n, s, demo, s.description)


def ev_consumer_sentiment_survey(n, v_age: str = '18-65', v_country_of_residence: str = "United Kingdom",
                                 v_income_level: str = "$25000 - $200000"):
    s = survey.Survey("EV_Consumer_Sentiment")
    s.description("Consumer Sentiment on Electric Vehicles (EVs)")
    # Section 1: Demographic Information
    s.add_multiple_choice_question("Age", ["Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or older"])
    s.add_multiple_choice_question("Gender",
                                   ["Male", "Female", "Non-Binary", "Prefer not to say", "Other: _________"])
    s.add_short_answer_question("Occupation:")
    s.add_multiple_choice_question("Income Level",
                                   ["Under $25,000", "$25,000 - $49,999", "$50,000 - $74,999", "$75,000 - $99,999",
                                    "$100,000 or more"])
    s.add_multiple_choice_question("Location", ["Urban", "Suburban", "Rural"])
    s.add_multiple_choice_question("Current Vehicle Ownership/Usage",
                                   ["Own a gasoline vehicle", "Own an electric vehicle", "Do not own a vehicle",
                                    "Prefer public transportation"])
    # Section 2: Awareness and Perception
    s.add_multiple_choice_question("Are you aware of Electric Vehicles (EVs)?", ["Yes", "No"])
    s.add_linear_scale_question("How would you rate your knowledge about EVs?", 1, 5)
    s.add_multiple_choice_question("What is your overall perception of EVs?",
                                   ["Positive", "Negative", "Neutral", "No opinion"])
    # Section 3: Purchase Consideration and Barriers
    s.add_multiple_choice_question("Have you considered purchasing an EV?", ["Yes", "No"])
    s.add_multiple_choice_question("What is the main factor that would encourage you to purchase an EV?",
                                   ["Environmental benefits", "Lower operating costs", "Technological features",
                                    "Government incentives", "Other: _________"])
    s.add_multiple_choice_question("What is the main factor that discourages you from purchasing an EV?",
                                   ["High purchase price", "Lack of charging infrastructure",
                                    "Limited driving range", "Limited model options", "Other: _________"])
    s.add_linear_scale_question("How important is the environmental impact in your vehicle purchasing decision?", 1,
                                5)
    # Section 4: Infrastructure and Accessibility
    s.add_linear_scale_question("How would you rate the accessibility of EV charging stations in your area?", 1, 5)
    s.add_multiple_choice_question(
        "Do you believe there is adequate infrastructure to support EV usage in your area?", ["Yes", "No"])
    # Section 5: Trust and Brand Perception
    s.add_multiple_choice_question("Which brand do you trust the most when it comes to purchasing an EV?",
                                   ["Tesla", "Chevrolet", "Nissan", "Ford", "BMW", "Other: _________"])
    s.add_linear_scale_question("How much do you trust the technology and safety of EVs?", 1, 5)
    # Section 6: Pricing and Value
    s.add_multiple_choice_question("Do you think EVs provide good value for their price?", ["Yes", "No"])
    s.add_multiple_choice_question("What is the maximum amount you would be willing to pay for an EV?",
                                   ["Under $25,000", "$25,000 - $34,999", "$35,000 - $44,999", "$45,000 - $54,999",
                                    "$55,000 or more"])
    demo = demgen.Demographic(
        age=v_age,  # variable
        country_of_residence=v_country_of_residence,  # variable
        income_level=v_income_level,  # variable
        social_media_usage='Moderate to high',
    )
    runner.get_simulation_data(n, s, demo, s.description)


def online_shopping_behavior_survey(n, v_age: str = '18-65', v_country_of_residence: str = "Belgium",
                                    v_income_level: str = "$40000 - $80000"):  # default dem param values if not specified for simulation
    s = survey.Survey("Online_Shopping_Behavior")
    s.description("Understanding Online Shopping Behavior During Sale Events",
                  "Imagine a popular online shopping platform is holding a significant sale event, featuring substantial discounts across various product categories (e.g., electronics, fashion, home goods) for 48 hours. Some of your favorite items and brands are listed at attractive prices.")
    # Section 1: Demographic Information
    s.add_multiple_choice_question("Age", ["Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or older"])
    s.add_multiple_choice_question("Gender",
                                   ["Male", "Female", "Non-Binary", "Prefer not to say", "Other: _________"])
    s.add_multiple_choice_question("Occupation", ["Option1", "Option2", "Option3", "Option4", "Other: _________"])
    # Section 2: Decision-Making Process
    s.add_linear_scale_question("How likely are you to participate in the sale event?", 1, 5)
    s.add_multiple_choice_question("What product categories are you most likely to explore first?",
                                   ["Electronics", "Fashion", "Home Goods", "Other: _________"])
    s.add_multiple_choice_question("Would you create a shopping list or budget prior to the sale?", ["Yes", "No"])
    s.add_linear_scale_question("How likely are you to make impulsive buying decisions during the sale?", 1, 5)
    # Section 3: Influence of Discounts and Offers
    s.add_multiple_choice_question("What minimum discount percentage would entice you to make a purchase?",
                                   ["Less than 10%", "10%", "20%", "30%", "40% or more"])
    s.add_multiple_choice_question("Do limited-time offers create a sense of urgency for you to make a purchase?",
                                   ["Yes", "No"])
    s.add_multiple_choice_question(
        "Are you likely to buy items you don’t immediately need because they are on sale?", ["Yes", "No"])
    # Section 4: Post-Purchase Behavior
    s.add_multiple_choice_question(
        "After making a purchase during a sale, how often do you experience buyer’s remorse?",
        ["Never", "Rarely", "Sometimes", "Often", "Always"])
    s.add_multiple_choice_question(
        "Are you likely to keep items that are non-essential or slightly unsatisfactory simply because they were on sale?",
        ["Yes", "No"])
    # Section 5: Social Influence and Peer Behavior
    s.add_linear_scale_question(
        "How likely are you to discuss the sale and potential purchases with friends or family before buying?", 1, 5)
    s.add_multiple_choice_question(
        "Does seeing others (e.g., friends, influencers) purchasing items during the sale influence your purchasing decisions?",
        ["Yes", "No"])
    # Section 6: Future Interaction
    s.add_multiple_choice_question(
        "Would a satisfactory experience during this sale make you more likely to shop during future sales?",
        ["Yes", "No"])
    s.add_multiple_choice_question(
        "If you miss out on a product during the sale, would you consider buying it at full price later?",
        ["Yes", "No"])
    demo = demgen.Demographic(
        country_of_residence=v_country_of_residence,  # variable
        income_level=v_income_level,  # variable
        shopping_preferences="Online shopping",
        social_media_usage='Moderate to high',
    )
    runner.get_simulation_data(n, s, demo, s.description)

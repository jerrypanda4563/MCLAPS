from app.internal import demgen, terminal, survey
from fastapi import FastAPI
from app.internal import simulation_runner as runner

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/simulations/pricing")
async def root(request_id: str, runs: int, age: str, country_of_residence, income_level: str):
    # do data validation

    # run the simulation async

    # get the output of the simulation to bubble

    # ideally just do data validation, send the request to queue and have a different service process them



    return {"message": "Hello World"}

def price_simulation(age: int, demographic: map, prompt: str):
    # fill the survey
    price_simulation()
    return


def price_simulation() -> survey.Survey:
    s = survey.Survey("price simulation")
    s.add_long_answer_question("what is the name of your company")
    return s


def new_price_demographic() -> demgen.Demographic:
    d = demgen.Demographic(gender_identity="female, male, queer")
    return d


def main():
    invictus_survey = survey.Survey("Osman Simulation")
    invictus_survey.add_long_answer_question(
        'What is the timescale and cost of MEP and HVAC installation jobs within buildings?')
    invictus_survey.add_long_answer_question(
        'In your experience, what are the factors negatively effecting the MEP and HVAC installation jobs within '
        'buildings?')
    invictus_survey.add_long_answer_question(
        'What specific technologies or tools do you utilize to enhance productivity and address these factors?')
    invictus_survey.add_long_answer_question(
        'Could you describe a recent project where you encountered significant physical challenges to do with these '
        'jobs?')
    invictus_survey.add_long_answer_question(
        'How open are you (or your organisation) to adopting new innovations and technology in your work? If so Have '
        'you adopted/implemented any?')

    demo = demgen.Demographic(country_of_residence='United Kingdom and Europe', employment_status='Full-time',
                              occupation=['construction builder', 'construction project manager',
                                          'construction project consultant', 'building services engineer'])
    runner.get_simulation_data(1, invictus_survey, demo)


if __name__ == "__main__":
    terminal.pricing_simulation(1)

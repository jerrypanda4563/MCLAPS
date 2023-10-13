import json
import csv
import os
from app.internal import survey


# Test initialization of Survey class
def test_survey_initialization():
    s = survey.Survey("Test Survey")
    assert s.name == "Test Survey"
    assert s.questions == []


# Test addition of a short answer question
def test_add_short_answer_question():
    s = survey.Survey("Test Survey")
    s.add_short_answer_question("What's your name?")
    assert s.questions[0]["type"] == "short answer"
    assert s.questions[0]["question"] == "What's your name?"


# Test addition of a multiple-choice question
def test_add_multiple_choice_question():
    s = survey.Survey("Test Survey")
    s.add_multiple_choice_question("Choose a color", ["Red", "Blue", "Green"])
    assert s.questions[0]["type"] == "multiple choice"
    assert s.questions[0]["choices"] == ["Red", "Blue", "Green"]


# Test conversion of questions to JSON
def test_to_json():
    s = survey.Survey("Test Survey")
    s.add_short_answer_question("What's your name?")
    json_data = s.to_json()
    assert json.loads(json_data) == s.questions


# Test creation of a CSV file
def test_create_csv(tmpdir):
    s = survey.Survey("Test Survey")
    s.add_short_answer_question("What's your name?")

    # Use pytest's temporary directory feature to avoid clutter
    filename = os.path.join(tmpdir, "output.csv")

    s.create_csv(filename)

    # Check that the file was created and has the expected content
    assert os.path.exists(filename)
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)
        assert headers == ["What's your name?"]


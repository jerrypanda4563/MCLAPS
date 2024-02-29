from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union

class DemographicModel(BaseModel):
    sex_at_birth: Optional[str] = None
    gender_identity: Optional[str] = None
    age: Optional[str] = None
    marital_status: Optional[str] = None
    sexual_orientation: Optional[str] = None
    nationality: Optional[str] = None
    country_of_residence: Optional[str] = None
    state_province: Optional[str] = None
    city: Optional[str] = None
    rural_or_urban: Optional[str] = None
    type_of_residence: Optional[str] = None
    length_of_residence: Optional[str] = None
    level_of_education: Optional[str] = None
    student_status: Optional[str] = None
    field_of_study: Optional[str] = None
    occupational_area: Optional[str] = None
    annual_income_level: Optional[str] = None
    employment_status: Optional[str] = None
    home_ownership: Optional[str] = None
    ethnicity: Optional[str] = None
    languages_spoken: Optional[str] = None
    religion: Optional[str] = None
    cultural_practices: Optional[str] = None
    immigration_status: Optional[str] = None
    hobbies_and_interests: Optional[str] = None
    shopping_motivations: Optional[str] = None
    shopping_habits: Optional[str] = None
    shopping_channels: Optional[str] = None
    shopping_frequency: Optional[str] = None
    dietary_preferences: Optional[str] = None
    physical_activity_levels: Optional[str] = None
    social_media_usage: Optional[str] = None
    travel_habits: Optional[str] = None
    alcohol_use: Optional[str] = None
    tobacco_and_vape_use: Optional[str] = None
    technology_usage: Optional[str] = None
    family_structure: Optional[str] = None
    household_size: Optional[str] = None
    number_of_children: Optional[str] = None
    pet_ownership: Optional[str] = None
    number_of_pets: Optional[str] = None
    relationship_status: Optional[str] = None
    caregiving_responsibilities: Optional[str] = None
    general_health_status: Optional[str] = None
    disabilities_or_chronic_illnesses: Optional[str] = None
    mental_health_status: Optional[str] = None
    health_insurance_status: Optional[str] = None
    access_to_healthcare: Optional[str] = None
    political_affiliation: Optional[str] = None
    voting_behavior: Optional[str] = None
    political_engagement: Optional[str] = None

    class Config:
        extra = "forbid"  # Forbids any extra fields not defined in the model

#survey validation model
class ShortAnswerQuestion(BaseModel):
    type: str = Field("short answer", Literal=True)
    question: str
    answer: Optional[str] = None

class LongAnswerQuestion(BaseModel):
    type: str = Field("long answer", Literal=True)
    question: str
    answer: Optional[str] = None

class MultipleChoiceQuestion(BaseModel):
    type: str = Field("multiple choice", Literal=True)
    question: str
    choices: List[str]
    answer: Optional[str] = None

class CheckboxesQuestion(BaseModel):
    type: str = Field("checkboxes", Literal=True)
    question: str
    choices: List[str]
    answer: Optional[List[str]] = None

class LinearScaleQuestion(BaseModel):
    type: str = Field("linear scale", Literal=True)
    question: str
    min_value: int
    max_value: int
    answer: Optional[int] = None

class SurveyModel(BaseModel):
    name: str
    description: Optional[str] = None
    questions: List[Union[ShortAnswerQuestion, LongAnswerQuestion, MultipleChoiceQuestion, CheckboxesQuestion, LinearScaleQuestion]]

    @validator('questions', each_item=True)
    def check_question_type(cls, v):
        if v.type not in ["short answer", "long answer", "multiple choice", "checkboxes", "linear scale"]:
            raise ValueError('Invalid question type')
        return v

class SimulationParameters(BaseModel):
    demographic_params: DemographicModel
    survey_params: SurveyModel
    n_of_runs: int
    workers: Optional[int] = 5
    class Config:
        extra="forbid"
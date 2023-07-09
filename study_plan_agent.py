
from api.learning.classes import SinglePromptAgent
from api.learning.actions import get_sections_from_study_plan, get_better_studyplan_description, separate_text
import os
from dotenv import load_dotenv

load_dotenv()

example_study_plan = '''
I want to learn basic html and css to build a website, the website must have an title that says: Welcome to my page! And after that an small description
'''


# def get_better_studyplan_description(study_plan_description: str):
#     _template = '''You are an useful teacher, your are in charge of building an awesome study plan
#     for a student. This is the student study plan: {study_plan_description}
    
#     Rewrite this description and included detailed information of the necessary steps to succcesful
#     get the objectives of the study plan.

#     To make your work the best follow this steps:

#     1. Think about which is the most important objective of the study plan
#     2. Think in way to structure the plan in sections with smaller objectives

#     Comments between ``` are to help you understand your task
#     Give your answer in the following format:

#     _start_
#     Study plan title ```Write a descriptive title for the study plan```

#     General objective ```Write here a general objective for the study plan```

#     ```In the part below write each section for the study plan mentioning an objective, anything else.```
#     Section_1_title
#         objective: 

#     Section_2_title
#         objective: 
#     ...

#     ```No more than ten sections are necessary, think about what is the best way to structure the plan```
#     _end_

#     The _start_ and _end_ tags are mandatory
#     '''

#     better_description_agent = SinglePromptAgent(template=_template)
#     return better_description_agent.run(study_plan_description=study_plan_description)


study_plan_description = get_better_studyplan_description(study_plan_description=example_study_plan)

def create_sections_from_studyplan(study_plan: str):
    sections = get_sections_from_study_plan(study_plan_description=study_plan_description)
    list_of_sections = separate_text(sections, '_separator_')
    for section in list_of_sections:
        [title, objective] = separate_text(section, '_title_')
    


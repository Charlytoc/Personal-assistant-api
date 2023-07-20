from api.learning.classes import SinglePromptAgent
from .models import Section, StudyPlan, Profile, User, Topic
from langchain.callbacks import get_openai_callback

def print_in_color(text, color):
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }

    if color.lower() in colors:
        color_code = colors[color.lower()]
        reset_code = colors['reset']
        print(f"{color_code}{text}{reset_code}")
    else:
        print(f"Invalid color '{color}'")


def get_user_profile(user: User) -> Profile:
    profile = Profile.objects.get(user=user)
    return profile


def get_better_studyplan_description(study_plan_description: str):
    _template = '''You are an useful teacher, your are in charge of building an awesome study plan
    for a student. This is what the student wants to learn: {study_plan_description}
    
    Write a great study plan based in the student requirements, the goals is to have an objective 
    of what to study next.

    To make your work the best follow this steps:

    1. Think about which is the most important objective of the study plan.
    2. Think in way to structure the plan in sections with smaller objectives

    Comments between ``` are to help you understand your task
    Give your answer in the following format:

    _start_
    Title of the study plan _tit_ ```Write a descriptive title for the study plan here and include the _tit_ tag to properly handle the title``` 
    
    The objective of this study plan is... ```Write here a general objective for the study plan, also make mention of steps to successfully reach the goals```

    We will get the hands on... ```Write an interesting description for the study plan```
    _end_

    The _start_, _end_ and _tit_ tags are mandatory. Always return your answer in the student language
    '''

    better_description_agent = SinglePromptAgent(template=_template)
    return better_description_agent.run(study_plan_description=study_plan_description)


def separate_text(text:str, separator:str):
    separated_text = text.split(separator)
    return separated_text

def get_sections_from_study_plan(study_plan_description: str):
    _template = '''You are an useful teacher, your are in charge of help an student to extend to write the necessary information
    section to successfully learn something in a study plan.

    This is the student study plan: {study_plan_description}
    
    Write the sections of the plan in an extended way to make it easy to investigate and execute
    succesfully the study plan.

    To make your work the best follow this steps:

    1. Think in the correct sections to divide in an incremental way the study plan
    2. Return the correct sections with an extended objective.

    Comments between ``` are to help you understand your task
    Give your answer in the following format:

    _start_
    Section 1: An awesome title for the section _tit_ ``Always include this _tit_ tag after each section title``
    Objective ``An objective to accomplish in this section``
    _separator_ ``Include always this _separator_ after each section to properly separate them after``
    Section 2: Another awesome title _tit_ ``Please remember to include _tit_
    Objective
    _end_

    The _start_,_end_, _tit_ and _separator_ tags are mandatory and its so important to add them. 
    Always return your answer in the student language.
    '''

    better_sections_agent = SinglePromptAgent(template=_template)
    return better_sections_agent.run(study_plan_description=study_plan_description)

def create_sections_from_studyplan(study_plan: StudyPlan):
    with get_openai_callback() as callback:
        sections = get_sections_from_study_plan(study_plan_description=study_plan.ai_description)
        print_in_color(sections, 'yellow')
        list_of_sections = separate_text(sections, '_separator_')
        for section in list_of_sections:
            separated_text = separate_text(section, '_tit_')

            if len(separated_text) != 2:
                print_in_color(f"Unexpected topic format: {section}", 'blue')
                print_in_color(f"This was received: {separated_text}", 'red')
                continue  # Skip this iteration and move to the next topic

            [title, objective] = separated_text

            title = title.strip()
            objective = objective.strip()

            new_section = Section.objects.create(
                title=title,
                objective=objective,
                study_plan=study_plan,
                created_by=study_plan.created_by
            )
        total_cost = callback.total_cost
        total_tokens = callback.total_tokens
        print_in_color(f'Spend: {total_cost} \n Tokens: {total_tokens}', 'red')
        return True


# First: Make a list of at least 5 different topics to separated the section, imagine each topics as a step of learning
# 
# TODO: I need to create different topics from a section, a topic needs to be no so much extensive


def get_topics_from_section(section_objective: str, section_title: str, study_plan_description: str):
    _template = '''You are an useful teacher.
    You are in charge of help a student to divide a section of a study plan into smaller pieces using a separator
    and indicating which is the title with some characters as you will see after.

    This is the student study plan: {study_plan_description}

    And this is the current working section.
    
    {section_title}
    {section_objective}

    To make your work the best follow this steps:

    1. Think how to divide the objective of the section into smaller topics
    2. Return the necessary topics with a simple objective each one

    Comments between ``` are to help you understand your task
    Give your answer in the following format:

    _start_
    Cool title for the first topic _tit_ ``Always include the _tit_ tag after each topic title``
    Topic objective
    _separator_ ``Include always this _separator_ after each topic objective to properly separate them after``
    Another cool title  _tit_ 
    Topic objective
    _separator_
    Topic title here _tit_
    topic objective
    _end_

    The _start_,_end_, _tit_ and _separator_ tags are mandatory and extremely important. Always return your answer in the student language
    '''

    topics_agent = SinglePromptAgent(template=_template)
    return topics_agent.run(study_plan_description=study_plan_description,
                             section_objective=section_objective, 
                             section_title=section_title)



def create_topics_for_a_section(section: Section):
    with get_openai_callback() as callback:
        topics = get_topics_from_section(study_plan_description=section.study_plan.ai_description, 
                                        section_title=section.title, 
                                        section_objective=section.objective)
        print_in_color(f'Got this topics from GPT: {topics}', 'blue')
        list_of_topics = separate_text(topics, '_separator_')
        print(f'Total number of topics: {len(list_of_topics)}')

        for topic in list_of_topics:
            separated_text = separate_text(topic, '_tit_')

            if len(separated_text) != 2:
                print_in_color(f"Unexpected topic format: {topic}", 'blue')
                print_in_color(f"This was received: {separated_text}", 'red')
                continue  # Skip this iteration and move to the next topic

            [title, objective] = separated_text
         
            title = title.strip()
            objective = objective.strip()
            new_topic = Topic.objects.create(
                title=title,
                objective=objective,
                explanation='EMPTY FOR THE MOMENT',
                created_by=section.created_by,
                section=section
            )
            get_topic_content(topic=new_topic)

        total_cost = callback.total_cost
        total_tokens = callback.total_tokens
        study_plan = section.study_plan
        print(study_plan.title, "THIS IS THE TITLE OF THE STUDY PLAN")
        study_plan.total_spent += total_cost
        print(section.total_spent)
        study_plan.save()
        print_in_color(f'Spend: {total_cost} \n Tokens: {total_tokens}', 'red')
    

def create_topics_for_all_studyplan_sections(study_plan: StudyPlan):
    with get_openai_callback() as callback:
            
        sections = study_plan.section_set.all()
        # for section in sections:
        #     topics = get_topics_from_section(study_plan_description=study_plan.ai_description, section_title=section.title, section_objective=section.objective)
        #     list_of_topics = separate_text(topics, '_separator_')
        #     for topic in list_of_topics:
        #         [title, objective] = separate_text(topic, '_title_')
        #         title = title.strip()
        #         objective = objective.strip()
        #         new_topic = Topic.objects.create(
        #             title=title,
        #             objective=objective,
        #             explanation='EMPTY FOR THE MOMENT',
        #             created_by=section.created_by
        #         )
        total_cost = callback.total_cost
        total_tokens = callback.total_tokens
        print(f'Spend: {total_cost} \n Tokens: {total_tokens}')
        return True
        
    
# def callback_how_to():
#     with get_openai_callback() as callback:
#         total_cost = callback.total_cost
#         total_tokens = callback.total_tokens



def get_topic_content(topic: Topic):
    _template = '''You are an super useful and kind teacher, your are in charge of building an awesome content
    for a certain topic in a student study plan. 
    
    This is the current section of the study plan: {section_description}

    This is the topic you need to write about: {topic_title}

    You can consider succesful your task if you are capable of explaining the topic to
    reach the objective: {topic_objective}
    
    Don't explain more than the needed for the topic.

    To make your work the best follow this steps:

    1. Think about a wonderful manner to explain for somebody with a clean and fun way
    2. Leave exercises to the student, at least two questions as a homework.

    Comments between ``` are to help you understand your task
    Give your answer in the following format:

    _start_
    ``Wonderful explanation of the topic, using a clean language, at least 350 words.``
    _end_

    The _start_ and _end_ tags are mandatory. Always return your answer in the student language
    '''
    topic_writter = SinglePromptAgent(template=_template)
    explanation = topic_writter.run(topic_objective=topic.objective, topic_title=topic.title, section_description=topic.section.objective)
    topic.explanation = explanation
    topic.save()
    # print_in_color()



def create_studyplan_description_from_studyplan(study_plan: StudyPlan):
    with get_openai_callback() as callback:
        ai_description = get_better_studyplan_description(study_plan.description)
        title, description = separate_text(ai_description, '_tit_')
        study_plan.ai_description = description
        study_plan.suggested_title = title

        study_plan.save()
        total_cost = callback.total_cost
        total_tokens = callback.total_tokens
        print_in_color(f'Spend: {total_cost} \n Tokens: {total_tokens}', 'red')
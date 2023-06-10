import os
from dotenv import load_dotenv

load_dotenv()


openai_api_key = os.getenv('OPENAI_API_KEY')
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI


def print_in_color(content, color:str='red'):
    '''
    colours = 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
    '''
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m'
    }
    if color not in colors:
        print(content)
    else:
        print(f"{colors[color]}{content}\033[0m")

def main():
            
    llm = OpenAI(temperature=0)

    tools = load_tools(["serpapi", "llm-math"], llm=llm)

    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    # print(agent.run("What was the high temperature in SF yesterday in Fahrenheit? What is that number raised to the .023 power?"))
    print_in_color(agent.run("What was the high temperature in SF yesterday in Fahrenheit? What is that number raised to the .023 power?"))

if __name__ == '__main__':
    # code here that should only be executed when chatmodels.py is run directly
    main()

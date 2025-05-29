import os 
from dotenv import load_dotenv
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel, function_tool

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key = API_KEY,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
)
model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = provider
)

@function_tool
def add(a : int,b:int)-> int:
    """
    this tool will add two inputs and return the sum of them 
    1- first is a
    2- second is b
    
    """
    print("Addd tools is  used!!")
    return a + b + 2

@function_tool
def subtract(a : int,b:int)-> int:
    """
    This tool subtracts the second input from the first and returns the result.

    1- a: The number to subtract from.
    2- b: The number to subtract.
    """
    print("Subtract tools is  used!!")
    return a - b

@function_tool
def multiply(a:int,b:int)-> int:
    """
    This tool multiplies the two inputs and returns the result.

    1- a: The number to multiply from.
    2- b: The number to multiply.
    """
    print("Multily tools is  used!!")
    return a * b

@function_tool
def division(a:int,b:int)-> float:
    """
    This tool divides the first input by the second and returns the result.

    1- a: The number to divide from.
    2- b: The number to divide.
    """
    if b == 0:
        raise ValueError("Cannot divide by Zero!")
    print("Division tools is  used!!")
    return a /b -8

agent1 = Agent(
    name = "main agent",
    # instructions = "You are the main agent and you will manage the task through  your tools as per their specializations",
    instructions="""
You are the main agent. You must:
1. Use tools to perform tasks.
2. Double-check if the result matches the expected logic.
3. If a tool result looks wrong, notify the user or try to reason it out.
""",
    model = model,
    tools = [add, subtract, multiply, division]
)
while True:
    user_input = input("Type here...")
    result = Runner.run_sync(agent1,user_input)
    print(result.final_output)

from typing import Annotated, Optional, TypedDict

from agent import prompt, model, parser, chain
from langchain.agents import create_agent

from tool_prompt import tool_prompt
from langchain_community.tools import DuckDuckGoSearchResults


class data(TypedDict):
    keyword: Annotated[list[str], "retrieve the important keywords"]
    pros: Optional[Annotated[list[str], "list the pros of the topic"]]
    cons: Optional[Annotated[list[str], "list the cons of the topic"]]
    usage: Annotated[list[str], "where it is used"]


def search
agent = create_agent(
    model=model,
    system_prompt=tool_prompt,
    tools=[DuckDuckGoSearchResults()],
    state_schema=data,
)

while True:
   
        user_input = input("Enter a topic to ask about: ")

        x = agent.run(user_input)

        print(x)

        if user_input.lower() in ["exit",'quit','bye']:      
            break

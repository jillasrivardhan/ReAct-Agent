
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


def search(query: str,) -> str:
    """
    Perform a DuckDuckGo search and return the results as a string.
    """
    search_tool = DuckDuckGoSearchResults()
    results = search_tool.run(query)
    return results

agent = create_agent(
    model=model,
    system_prompt=tool_prompt,
    tools=[search],
    state_schema=data,
)

while True:
   
        user_input = input("Enter a topic to ask about: ")

        x = agent.run(user_input)

        print(x)

        if user_input.lower() in ["exit",'quit','bye']:      
            break

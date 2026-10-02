
from typing import Annotated, Optional, TypedDict

from agent import prompt, model, parser, chain
from langchain.agents import create_agent


class data(TypedDict):
    keyword: Annotated[list[str], "retrieve the important keywords"]
    pros: Optional[Annotated[list[str], "list the pros of the topic"]]
    cons: Optional[Annotated[list[str], "list the cons of the topic"]]
    usage: Annotated[list[str], "where it is used"]


agent = create_agent(
    model=model,
    system_prompt=prompt,
    tools=[],
    state_schema=data,
)

x = agent.run()

print(x)
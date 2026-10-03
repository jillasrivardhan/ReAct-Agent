
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
    search_tool = DuckDuckGoSearchResults(max_results=3)
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

# from langchain.agents import create_react_agent, AgentExecutor
# from langchain import hub
# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(model="gpt-4")
# tools = [duckduckgo_search]
# prompt = hub.pull("hwchase17/react")
# agent = create_react_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

# result = agent_executor.invoke({"input": "What is the capital of France?"})
# print(result["output"])   
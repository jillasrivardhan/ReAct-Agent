# agent.py

from typing import Literal

from ddgs import DDGS

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (RunnableBranch,RunnableLambda,RunnablePassthrough)
from langchain_core.tools import tool

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

from prompts import (
    ROUTER_PROMPT,
    DIRECT_SYSTEM_PROMPT,
    REACT_SYSTEM_PROMPT,
)


# ============================================================
# 1. LLM MODEL
# ============================================================

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)


# ============================================================
# 2. ROUTER CHAIN
# ============================================================

router_prompt = ChatPromptTemplate.from_template(
    ROUTER_PROMPT
)

router_chain = (
    router_prompt
    | model
    | StrOutputParser()
)


# ============================================================
# 3. DIRECT LLM CHAIN
# ============================================================

direct_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", DIRECT_SYSTEM_PROMPT),
        ("human", "{question}"),
    ]
)

direct_chain = (
    direct_prompt
    | model
    | StrOutputParser()
)


# ============================================================
# 4. DUCKDUCKGO SEARCH TOOL
# ============================================================

@tool
def search(query: str) -> str:
    """
    Search DuckDuckGo for current or external information.

    Args:
        query: A plain text search query.
    """

    if not isinstance(query, str):
        query = str(query)

    query = query.strip()

    if not query:
        return "Search query cannot be empty."

    try:
        results = DDGS().text(
            query=query,
            max_results=3
        )

        if not results:
            return "No search results found."

        formatted_results = []

        for result in results:
            formatted_results.append(
                f"Title: {result.get('title', '')}\n"
                f"URL: {result.get('href', '')}\n"
                f"Content: {result.get('body', '')}"
            )

        return "\n\n".join(formatted_results)

    except Exception as error:
        return f"Search failed: {error}"

tools = [search]


# ============================================================
# 5. LANGCHAIN REACT AGENT
# ============================================================

react_agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=REACT_SYSTEM_PROMPT,
)


# ============================================================
# 6. RUN REACT AGENT
# ============================================================

def run_react_agent(inputs: dict) -> str:
    """
    Run the ReAct agent and return the final AI response.
    """

    result = react_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": inputs["question"],
                }
            ]
        }
    )

    messages = result.get("messages", [])

    # Find the last AI message that is not requesting a tool call.
    for message in reversed(messages):

        if getattr(message, "type", None) == "ai":

            tool_calls = getattr(
                message,
                "tool_calls",
                []
            )

            if not tool_calls:

                content = message.content

                # Usually content is a string.
                if isinstance(content, str):
                    return content

                # Handle structured content if returned.
                return str(content)

    return "The agent could not produce a final answer."


react_chain = RunnableLambda(
    run_react_agent
)


# ============================================================
# 7. ROUTE NORMALIZATION
# ============================================================

def normalize_route(
    value: str
) -> Literal["TOOL", "DIRECT"]:
    """
    Normalize the router response.

    TOOL   -> Use the ReAct agent.
    DIRECT -> Use the normal LLM.
    """

    route = value.strip().upper()

    if route.startswith("TOOL"):
        return "TOOL"

    return "DIRECT"


# ============================================================
# 8. ADD ROUTE TO INPUT
# ============================================================

routing_chain = RunnablePassthrough.assign(
    route=(
        router_chain
        | RunnableLambda(normalize_route)
    )
)


# ============================================================
# 9. RUNNABLE BRANCH
# ============================================================

branch = RunnableBranch(
    (
        lambda x: x["route"] == "TOOL",
        react_chain,
    ),
    direct_chain,
)


# ============================================================
# 10. COMPLETE ROUTING PIPELINE
# ============================================================

chain = routing_chain | branch


# ============================================================
# 11. MAIN ASK FUNCTION
# ============================================================

def ask(question: str) -> str:
    """
    Send a question to the routing pipeline.

    The router decides whether:
    - DIRECT -> normal LLM
    - TOOL   -> LangGraph ReAct agent
    """

    return chain.invoke(
        {
            "question": question
        }
    )


# ============================================================
# 12. CLI APPLICATION
# ============================================================

def main():

    print("=" * 60)
    print("        LangGraph ReAct Research Assistant")
    print("=" * 60)
    print("Ask a question.")
    print("Type 'exit', 'quit', or 'bye' to stop.")
    print("=" * 60)

    while True:

        user_input = input("\nYou: ").strip()

        # ----------------------------------------
        # Exit condition
        # ----------------------------------------

        if user_input.lower() in {
            "exit",
            "quit",
            "bye"
        }:

            print("\nAssistant: Goodbye!")
            break

        # ----------------------------------------
        # Empty input
        # ----------------------------------------

        if not user_input:

            print(
                "Assistant: Please enter a question."
            )

            continue

        # ----------------------------------------
        # Run agent
        # ----------------------------------------

        try:

            answer = ask(user_input)

            print(
                f"\nAssistant: {answer}"
            )

        except Exception as error:

            print(
                f"\nAn error occurred: {error}"
            )


# ============================================================
# 13. ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
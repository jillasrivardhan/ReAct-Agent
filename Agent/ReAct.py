from typing import Literal

from ddgs import DDGS

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnablePassthrough,
)
from langchain_core.tools import tool

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from prompts import (
    ROUTER_PROMPT,
    DIRECT_SYSTEM_PROMPT,
    REACT_SYSTEM_PROMPT,
)


# ============================================================
# 1. CREATE OPENAI MODEL
# ============================================================
# IMPORTANT:
# Do NOT create ChatOpenAI outside a function.
#
# The user enters their own API key in Streamlit.
# This function creates the model only AFTER receiving
# that user's API key.
# ============================================================

def get_model(api_key: str):

    if not api_key:
        raise ValueError(
            "OpenAI API key is required."
        )

    return ChatOpenAI(
        model="gpt-4.1-mini",
        api_key=api_key,
        temperature=0,
        max_retries=1,
        timeout=30,
    )


# ============================================================
# 2. ROUTER CHAIN
# ============================================================

def create_router_chain(api_key: str):

    model = get_model(api_key)

    router_prompt = ChatPromptTemplate.from_template(
        ROUTER_PROMPT
    )

    router_chain = (
        router_prompt
        | model
        | StrOutputParser()
    )

    return router_chain


# ============================================================
# 3. DIRECT LLM CHAIN
# ============================================================

def create_direct_chain(api_key: str):

    model = get_model(api_key)

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

    return direct_chain


# ============================================================
# 4. DUCKDUCKGO SEARCH TOOL
# ============================================================

@tool
def search(query: str) -> str:
    """
    Search DuckDuckGo for current or external information.

    Use this tool when the user asks for:
    - Current information
    - Latest information
    - News
    - Recent releases
    - External information
    - Information that may have changed
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

            title = result.get(
                "title",
                ""
            )

            url = result.get(
                "href",
                ""
            )

            body = result.get(
                "body",
                ""
            )

            formatted_results.append(
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Content: {body}"
            )

        return "\n\n".join(
            formatted_results
        )

    except Exception as error:

        return (
            f"Search failed: {error}"
        )


tools = [
    search
]


# ============================================================
# 5. CREATE REACT AGENT
# ============================================================

def create_react_agent(
    api_key: str
):

    model = get_model(
        api_key
    )

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=REACT_SYSTEM_PROMPT,
    )

    return agent


# ============================================================
# 6. RUN REACT AGENT
# ============================================================

def run_react_agent(
    inputs: dict
) -> str:

    question = inputs[
        "question"
    ]

    api_key = inputs[
        "api_key"
    ]

    if not api_key:
        raise ValueError(
            "OpenAI API key is required."
        )

    # Create the ReAct agent using
    # THIS USER'S API KEY.
    agent = create_react_agent(
        api_key
    )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
    )

    messages = result.get(
        "messages",
        []
    )

    # Get the last AI response
    for message in reversed(
        messages
    ):

        if getattr(
            message,
            "type",
            None
        ) == "ai":

            tool_calls = getattr(
                message,
                "tool_calls",
                []
            )

            # We want the final AI response,
            # not an AI message requesting a tool.
            if not tool_calls:

                content = message.content

                if isinstance(
                    content,
                    str
                ):

                    return content

                # Handle structured content
                if isinstance(
                    content,
                    list
                ):

                    text_parts = []

                    for part in content:

                        if isinstance(
                            part,
                            dict
                        ):

                            if part.get(
                                "type"
                            ) == "text":

                                text_parts.append(
                                    part.get(
                                        "text",
                                        ""
                                    )
                                )

                    if text_parts:

                        return "\n".join(
                            text_parts
                        )

                return str(
                    content
                )

    return (
        "The agent could not "
        "produce a final answer."
    )


# Convert the function into
# a Runnable.
react_chain = RunnableLambda(
    run_react_agent
)


# ============================================================
# 7. ROUTE NORMALIZATION
# ============================================================

def normalize_route(
    value: str
) -> Literal[
    "TOOL",
    "DIRECT"
]:

    route = value.strip().upper()

    if route.startswith(
        "TOOL"
    ):

        return "TOOL"

    return "DIRECT"


# ============================================================
# 8. CREATE COMPLETE ROUTING CHAIN
# ============================================================

def create_chain(
    api_key: str
):

    if not api_key:

        raise ValueError(
            "OpenAI API key is required."
        )

    # Router uses user's API key
    router_chain = create_router_chain(
        api_key
    )

    # Direct chain uses user's API key
    direct_chain = create_direct_chain(
        api_key
    )

    # Add route to the existing input.
    #
    # The input remains:
    #
    # {
    #     "question": "...",
    #     "api_key": "..."
    # }
    #
    # and gets:
    #
    # {
    #     "question": "...",
    #     "api_key": "...",
    #     "route": "DIRECT/TOOL"
    # }

    routing_chain = (
        RunnablePassthrough.assign(
            route=(
                router_chain
                | RunnableLambda(
                    normalize_route
                )
            )
        )
    )

    # ========================================================
    # ROUTING
    # ========================================================

    branch = RunnableBranch(

        # ----------------------------------------------------
        # TOOL ROUTE
        # ----------------------------------------------------

        (
            lambda x:
                x["route"] == "TOOL",

            react_chain,
        ),

        # ----------------------------------------------------
        # DEFAULT = DIRECT
        # ----------------------------------------------------

        direct_chain,
    )

    # ========================================================
    # COMPLETE PIPELINE
    # ========================================================

    chain = (
        routing_chain
        | branch
    )

    return chain


# ============================================================
# 9. MAIN ASK FUNCTION
# ============================================================

def ask(
    question: str,
    api_key: str
) -> str:

    if not question:
        raise ValueError(
            "Question cannot be empty."
        )

    if not api_key:
        raise ValueError(
            "OpenAI API key is required."
        )

    # Create the complete chain using
    # the current user's API key.
    chain = create_chain(
        api_key
    )

    # Send both question and API key
    # through the pipeline.
    response = chain.invoke(
        {
            "question": question,
            "api_key": api_key,
        }
    )

    return response


# ============================================================
# 10. CLI APPLICATION
# ============================================================

def main():

    print("=" * 60)

    print(
        "       LangGraph ReAct Research Assistant"
    )

    print("=" * 60)

    print(
        "\nEnter your OpenAI API key."
    )

    api_key = input(
        "OpenAI API Key: "
    ).strip()

    if not api_key:

        print(
            "\nOpenAI API key is required."
        )

        return

    print(
        "\nAsk a question."
    )

    print(
        "Type 'exit', 'quit', or 'bye' to stop."
    )

    print("=" * 60)

    while True:

        user_input = input(
            "\nYou: "
        ).strip()

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if user_input.lower() in {
            "exit",
            "quit",
            "bye",
        }:

            print(
                "\nAssistant: Goodbye!"
            )

            break

        # ----------------------------------------------------
        # EMPTY INPUT
        # ----------------------------------------------------

        if not user_input:

            print(
                "Assistant: "
                "Please enter a question."
            )

            continue

        # ----------------------------------------------------
        # RUN
        # ----------------------------------------------------

        try:

            answer = ask(
                user_input,
                api_key
            )

            print(
                f"\nAssistant: {answer}"
            )

        except Exception as error:

            print(
                f"\nAn error occurred: {error}"
            )


# ============================================================
# 11. ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
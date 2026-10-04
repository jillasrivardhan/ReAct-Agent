
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

prompt = PromptTemplate(
   template = "answer about the {topic} in a simple , concise, and clear manner. Use examples if possible. If you don't know the answer, say 'I don't know'.",
   input_variables = ["topic"]
)

model = ChatOllama(
   model= "qwen2.5:3b",
   temperature=0.2
)

parser = StrOutputParser()

chain = RunnableSequence(
   
      prompt,
      model,
      parser
   
)

user_input = input("enter a topic to ask about: ")

response = chain.invoke({"topic":user_input})

print(response)

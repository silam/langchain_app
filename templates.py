from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
model = ChatOpenRouter(
    model=os.getenv("MODEL")    
)

template = PromptTemplate(template="Write an article about {topic} ") 

# response1 = template.invoke({"topic":"AI"})
# response2 = template.invoke({"topic":"Cybersecurity"})

# print(f"AI: {response1.content}")

chain = template | model | StrOutputParser()
print(chain.invoke({"topic":"AI"}))
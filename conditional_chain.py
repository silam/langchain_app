from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableBranch, chain

load_dotenv()

class Feedback(BaseModel):
    customer_name: str = Field(
        description="The name of the customer providing feedback."
    )
    sentiment: Literal["positive", "negative"] = Field(
        description="The sentiment provided by the user. It can be either 'positive' or 'negative'."
    )

pyparser = PydanticOutputParser(pydantic_object=Feedback)

model = ChatOpenRouter(
    model=os.getenv("MODEL")    
)

prompt1 = PromptTemplate(template="""Analyze the following user feedback and determine if the sentiment is positive or negative: \n {feedback} \n {format_instruction}""", 
                         input_variables=["feedback"], validate_template=True, partial_variables={"format_instruction": pyparser.get_format_instructions()}) 



chain1 = prompt1 | model | pyparser

positive_email_prompt = PromptTemplate(template="""Write a professional and friendly email response to the following positive feedback about new iphone17: \n {feedback}""", input_variables=["feedback"], validate_template=True)
negative_email_prompt = PromptTemplate(template="""Write a professional and empathetic email response to the following negative feedback about new iphone17: \n {feedback}""", input_variables=["feedback"], validate_template=True)    


branch_chain = RunnableBranch(
    (lambda x: x.sentiment == "positive", positive_email_prompt | model | StrOutputParser()),
    (lambda x: x.sentiment == "negative", negative_email_prompt | model | StrOutputParser()),
    (lambda x: "Not able to analyze sentiment")
)

chain = chain1 | branch_chain

print(chain.invoke({"feedback": "I love the new iphone17! The camera quality is amazing and the battery life is impressive. Great job! - Name: Si Lam"}))
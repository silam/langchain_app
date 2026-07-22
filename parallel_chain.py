from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableBranch, chain, RunnableParallel

load_dotenv()

prompt1 = PromptTemplate(template="""Write a beginner friendly article on {topic}""",                         
                         input_variables=["topic"], validate_template=True)



prompt2 = PromptTemplate(template="""Generate a strong professional post with a strong hook on the following 
 topic: {topic}""",                         
                         input_variables=["topic"], validate_template=True)


prompt3 = PromptTemplate(template="""Merge provided article and linkedin post 
into a single document {article} and {post}""",
              
                         input_variables=["article", "post"], validate_template=True)

model = ChatOpenRouter(
    model=os.getenv("MODEL")    
)

parallel_chain = RunnableParallel(
    {
        'article': prompt1 | model | StrOutputParser(),
        'post': prompt2 | model | StrOutputParser()
    }
)
document_chain = prompt3 | model | StrOutputParser()

chain = parallel_chain | document_chain

print(chain.invoke({"topic": "AI discruption in IT"}))

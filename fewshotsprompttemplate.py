from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableBranch, chain, RunnableParallel

load_dotenv()

import os

load_dotenv()

model = ChatOpenRouter(
    model=os.getenv("MODEL")
)

examples = [
    {
        "ticket": "My invoice shows a charge I don't recognize from last month.",
        "output": "CATEGORY: billing \n PRIORITY: P2 \n TEAM: finance-ops \n SUMMARY: Unrecognized charge on invoice",
    },
    {
        "ticket": "The app crashes every time I try to upload a photo larger than 5MB.",
        "output": "CATEGORY: bug \n PRIORITY: P1 \n TEAM: mobile-eng \n SUMMARY: Crash on photo upload >5MB",
    },
    {
        "ticket": "Can you add dark mode to the settings page?",
        "output": "CATEGORY: feature-request \n PRIORITY: P4 \n TEAM: product \n SUMMARY: Request for dark mode",
    },
]

example_prompt = PromptTemplate(
    template="Ticket {ticket}\n{output}",
    input_variables=["ticket", "output"]
)

fewshot_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="You are a ticket triage assistant for our internal system. Classify each ticket using our exact schema: CATEGORY, PRIORITY (P1-P4), TEAM, SUMMARY. TEAM must be one of: finance-ops, mobile-eng, backend-eng, product, security.",
    suffix="Ticket: {ticket}",
    input_variables=["ticket"]
)

chain = fewshot_template | model | StrOutputParser()
print(chain.invoke({'ticket': "Users are seeing other people's account data on login"}))

# prompt = fewshot_template.invoke({'ticket': "Users are seeing other people's account data on login"})
# print(prompt)

# Output is:
# CATEGORY: security  
# PRIORITY: P1  
# TEAM: security  
# SUMMARY: Users seeing other people's account data on login
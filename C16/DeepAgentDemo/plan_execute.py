import json
import sqlite3

## Annotated in Python is a feature that allows developers to attach metadata 
## to type hints. This is particularly useful for enhancing code readability 
# and providing additional context about the types used in functions or variables.

from typing import TypedDict, List, Literal, Annotated
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.types import TypedDictType, Send, interrupt, Command
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class Step(BaseModel):
    id: int
    description: str
    depends_on : List[int] = Field(default_factory=list)
    sensitive: bool = Field(default=False, description="Requires human approval")

class Plan(BaseModel):
    steps: List[Step] = Field(default_factory=list)

class FinalAnswer(BaseModel):
    response: str
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence level of the response")

planner_llm = llm.with_structured_output(Plan)
final_llm = llm.with_structured_output(FinalAnswer)

#------- State -----------------

def merge_results(a: TypedDict, b: TypedDict) -> TypedDict:
    return {**a, **b}
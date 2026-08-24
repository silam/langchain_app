import json
import sqlite3

## Annotated in Python is a feature that allows developers to attach metadata 
## to type hints. This is particularly useful for enhancing code readability 
# and providing additional context about the types used in functions or variables.

from typing import TypedDict, Dict, List, Literal, Annotated
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
from typing import TypedDict, Dict, List, Literal, Annotated

def merge_results(a: Dict, b: Dict) -> Dict:
    return {**a, **b}

class State(TypedDict):
    objective: str
    plan: List[str]
    results: Annotated[Dict[int, str], merge_results]
    skipped: Annotated[Dict[int, str], merge_results]
    final: dict


#------------ Step with Retry -----------------
def run_step(description: str, context: str, retries: int = 2) -> str:
    last_err = ""
    for attempt in range(retries+1):
        try:
            msg = llm.invoke(
                f"Execute this step and return only the result.\n"
                f"Step: {description}\nContext:\n{context}"
            )
            if not msg.content.strip():
                raise ValueError("Empty response from LLM")
            return msg.content.strip()
        except Exception as e:
            last_err = str(e)
    raise RuntimeError(f"Failed to run step after {retries+1} attempts. Last error: {last_err}")    


def plan_node(state: State) -> State:
    if state.get("plan"):
        return {}
    plan = planner_llm.invoke(
        f"Break this objective into minimal dependent steps. Mark any step"
        f"that delete data, sends message, or spends money as sensitive.\n\n"
        f"Objective: {state.get('objective')}"
    )
    return {"plan": [step.model_dump() for step in plan.steps]}


def ready_steps(state: State) -> List[dict]:
    done = set(state.get("results", {}).keys()) | set(state.get("skipped", {}).keys())
    ready = []
    for s in state["plan"]:
        if s["id"] in done:
            continue
        ready.append(s)

        if all(d in done for d in s["depends_on"]):
            ready.append(s)
    return ready

def dispatch(state: State):
    ready = ready_steps(state)
    if not ready:
        return "Finalize"
    return [Send("execute", {"step": s, "state_results": state.get("results",{})}) for s in ready]

def execute(payload: dict) -> State:
    step = payload["step"]
    context = json.dumps(payload["state_results"], indent=2)

    if step["sensitive"]:
        decision = interrupt({
            "prompt": f"Approve sensitive step #{step['id']}?",
            "description": step["description"]
        })




    
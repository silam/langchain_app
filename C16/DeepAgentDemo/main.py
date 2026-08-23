from typing import TypedDict, List, Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_openrouter import ChatOpenRouter

from dotenv import load_dotenv


load_dotenv()

llm = ChatOpenRouter(model="gpt-4o-mini")

class Critique(BaseModel):
    clarity: int = Field(ge=1, le=10)
    coherence: int = Field(ge=1, le=10)
    engagement: int =Field(ge=1, le=10)
    feedback: str=Field(description="Specifi, actionable improvment")
    @property
    def total(self)->int:
        return self.clarity + \
                self.coherence + \
                self.engagement

class Revision(TypedDict):
    round: int
    draft: str
    critique: Critique
    
class State(TypedDict):
    task: str
    draft: str
    critique: Critique
    history : List[Revision]
    round : int



# //Structured output allows agents to return data in a specific, 
# predictable format. 
# //Instead of parsing natural language responses, 
# //you get structured data in the form of JSON objects, 
# //Pydantic models,
# //or dataclasses that your application can use directly.
critic_llm = llm.with_structured_output(Critique)


def generate(state: State) -> State:
    if not state["history"]:
        prompt = f"Write a draft for the task: {state['task']}"
    else:
        prompt = f"Task:\n{state['task']}\n\n Previous Draft: \n{state['critique'].feedback}"

    draft = llm.invoke(prompt).content
    return {"draft": draft, "round": state["round"] + 1}

def critique(state: State) -> State:
    result = critic_llm.invoke(
        f"Critique this draft against the task. Score clarity, coherence, engagement (1-10) and give the feedback. Task: \n\n{state['task']} \n\n Draft: \n{state['draft']}"
    )

    entry: Revision = {
        "round": state["round"],
        "draft": state["draft"],
        "critique": result
    }
    return {"critique": result, "history" : state["history"] + [entry]}

THRESHOLD = 27
MAX_ROUNDS = 4
        
def should_continue(state: State) -> Literal["generate","__end__"]:
    if state["critique"].total >= THRESHOLD or state["round"] >= MAX_ROUNDS:
        return END
    return "generate"
    
   
graph = StateGraph(State)
graph.add_node("generate", generate)
graph.add_node("critique", critique)
graph.add_edge(START, "generate")
graph.add_edge("generate", "critique")
graph.add_conditional_edges("critique", should_continue)
app = graph.compile()

def main():
    task = input("Enter the task: ")
    final = app.invoke({"task": task, "history": [], "round": 0})

    for rev in final["history"]:
        c = rev["critique"]
        print(f"\n{'='*60}\nROUND {rev['round']}")
        print(f"{'='*60}\n{rev['draft']}")
        print(f"\nScores  clarity={c.clarity}  coherence={c.coherence}  "
              f"engagement={c.engagement}  total={c.total}/30")
        print(f"Feedback: {c.feedback}")

    print(f"\n{'#'*60}\nFINAL DRAFT (round {final['round']})\n{'#'*60}")
    print(final["draft"])

if __name__ == "__main__":
    main()
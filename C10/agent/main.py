from psycopg import pq
from langgraph.checkpoint.postgres import PostgresSaver
from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenRouter(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

DB_URI = "postgresql://postgres:Fifa2014@localhost:5434/conversationdb?sslmode=disable"

with PostgresSaver.connect(DB_URI) as checkpointer:
    checkpointer.setup()
    agent = create_agent(
        model=llm,
        system_prompt="""
        You are an AI chat assitant who answers queries with a bit of humour. Use emojis to decorate your responses. Be
        polite and professional.
        """,
        checkpointer=checkpointer
    )

while True:
    user_input = input("You: ")
    if user_input.lower()=="exit":
        break
    response = agent.invoke(
        {
            "messages": [
                {"role":"user", "content": user_input}
            ]
        }, config={"configurable": {"thread_id": 1}}
    )

    print(response["messages"][-1].content)
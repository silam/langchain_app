from psycopg import pq
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain_community.tools import TavilySearch
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os
import requests


load_dotenv()


tavily_tool = TavilySearch(max_results=5)

    
llm = ChatOpenRouter(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
def getWeatherInfo(city: str):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": os.getenv("WEATHER_API_KEY"),
        "units": "metric"
    }

    response = requests.get(url, params)

    if response.status_code != 200:
        return f"Unable to fetch data from weather api"
    return response.json()


agent = create_agent(
    model=llm,
    system_prompt="""
    You are a weather AI agent who answers queries with a bit of humour. Use emojis to decorate your responses. Be
    polite and professional. Do not answer any questions other than weather related queries.
    """,
    checkpointer=InMemorySaver(),
    tools=[getWeatherInfo, tavily_tool]
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
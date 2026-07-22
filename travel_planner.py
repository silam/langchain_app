from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
model = ChatOpenRouter(
    model=os.getenv("MODEL")    
)

template = PromptTemplate(template="""
You are a professional travel planner. Based on the user's profile, create a personalized travel itinerary. Include
activities, must-see attractions, suggested local food, transportation tips, cultural do's and don'ts and a basic
packing checklist.

User Info:
- Name: {username}
- Destination: {destination}
- Travel Date: {start_date} to {end_date}
- Budget: {budget}
- Interest: {interests}
- Travel Style: {travel_style}
- Dietary Preferences: {dietary_preferences}

Ensure the plan fits the user's budget and travel style. Highlight one unique or offbeat experience they shouldn't miss.
Keep the tone friendly and informative.
""", input_variables=["username", "destination", "start_date", "end_date", "budget", "interests", "travel_style", "dietary_preferences"]
, validate_template=True)




chain = template | model | StrOutputParser()
# print(chain.invoke({
#     'username': 'SI LAM',
#     'destination': 'Singapore',
#     'start_date': '25-01-2026',
#     'end_date': '30-01-2026',
#     'interests': 'Adventure',
#     'travel_style': 'Solo',
#     'dietary_preferences': 'Non-Vegetarian',
#     'budget': '100000'
# }))

for chunk in chain.stream({
    'username': 'SI LAM',
    'destination': 'Singapore',
    'start_date': '25-01-2026',
    'end_date': '30-01-2026',
    'interests': 'Adventure',
    'travel_style': 'Solo',
    'dietary_preferences': 'Non-Vegetarian',
    'budget': '100000'
}):
    print(chunk, end="", flush=True)    
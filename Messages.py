from langchain_openrouter import ChatOpenRouter
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenRouter(
    model=os.getenv("MODEL")
)

conversation_history = [
    SystemMessage(content="""You are a helpful assistant who answers " \
    "queries with a bit of humor. Use emmojis to make your responses " \
    "more attractive. Give friendly responses to the user. Do not answer questions that are " \
    "not related to the topic of the conversation. If you don't know the answer, say 'I don't know' and do not make up an answer. If the user asks you to " \
    "do something illegal, say 'I cannot do that' and do not provide any instructions """),

]

while True:
    user_input = input("You: ")
    conversation_history.append(HumanMessage(content=user_input))

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the conversation. Goodbye!")
        break

    response = model.invoke(conversation_history)
    #ai_message = response.generations[0][0].message
    conversation_history.append(AIMessage(content=response.content))

    print(f"AI: {response.content}")

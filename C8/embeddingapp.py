from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, FewShotPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from typing import Literal
from openrouter import OpenRouter
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableBranch, chain, RunnableParallel
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv(override=True)

# with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
#     response = client.chat.send(
#     model = "openai/gpt-4o-mini",
#     messages = [
#         {"role": "user", "content": "Give me a motivational quote"},  
#     ],
#     max_tokens = 500
# )
#     print(response)

def generate_embedding(text: str):
    with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
        response = client.embeddings.generate(
            model="openai/text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

docs = [
    "The quick brown fox jumps over the lazy dog.",
    "A journey of a thousand miles begins with a single step.",
    "To be or not to be, that is the question.",
    "All that glitters is not gold.",
    "I think, therefore I am.",
    "Effel Tower is located in Paris, France.",
    "The Great Wall of China is one of the Seven Wonders of the World.",
    "Statue of Liberty is a symbol of freedom in the United States.",
    "Mount Everest is the highest mountain in the world."
]


query = "Where is the Eiffel Tower located?"
doc_embeddings = [generate_embedding(doc) for doc in docs]
query_embedding = generate_embedding(query)

similarities = cosine_similarity([query_embedding], doc_embeddings)
most_similar_doc_index = similarities.argmax()
most_similar_doc = docs[most_similar_doc_index]
print(most_similar_doc) 

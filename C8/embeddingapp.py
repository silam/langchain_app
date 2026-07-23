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

with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
    client.chat.send(
    model = "openai/gpt-4o-mini",
    messages = [
        {"role": "user", "content": "Give me a motivational quote"},  
    ],
    max_tokens = 500
)

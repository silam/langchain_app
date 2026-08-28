from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import os
from langchain_openrouter import ChatOpenRouter


from streamlit import status

load_dotenv(override=True)

app = FastAPI()

client = ChatOpenRouter(api_key=os.getenv("OPENROUTER_API_KEY"))    



class PromptRequest(BaseModel):
    name: str

class PromptResponse(BaseModel):
    message: str        
    model: str
    status : str


def stream_response(message: str):
    stream = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
          {"role": "user", "content": message}],
          stream = True
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content

@app.post("/generate")
def generate(prompt_request: PromptRequest):
    return StreamingResponse(stream_response(prompt_request.name), 
                             media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("streaming:app", host="0.0.0.0", port=8000, reload=True )
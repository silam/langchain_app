from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import os

load_dotenv(override=True)

app = FastAPI()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing")

client = OpenAI(api_key=api_key)



class PromptRequest(BaseModel):
    name: str

class PromptResponse(BaseModel):
    message: str        
    model: str
    status : str


def stream_response(message: str):
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}],
        stream=True,
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
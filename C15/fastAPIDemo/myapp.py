from fastapi import FastAPI, Query
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()



client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class PromptResponse(BaseModel):   
    response: str
    model: str
    status: str

@app.get("/generate")
def generate_prompt(request: str = Query(..., description="User prompt text")) -> PromptResponse:
    prompt = request.strip('"')
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    return PromptResponse(
        response=response.choices[0].message.content,
        model=response.model,
        status="success"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("myapp:app", host="localhost", port=8000, reload=True)
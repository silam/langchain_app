from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#http://127.0.0.1:8000/products?example=33
@app.get("/products")
def get_product(example: str):
    return {"name": "laptop", "price": 1234.55}

@app.get("/login")
def login():
    return {"message": "Please log in"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
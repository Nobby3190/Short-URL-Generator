import uvicorn
from fastapi import FastAPI
from utils import hash_url, retrieve_url_by_hashed_url

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.post("/get-url")
def get_url(hashed_url: str):
    url = retrieve_url_by_hashed_url(str(hashed_url))
    return {"url": url}


@app.post("/generate-url")
def generate_hashed_url(url: str):
    url = hash_url(str(url))
    return {"hashed_url": url}


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)

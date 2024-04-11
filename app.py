import uvicorn
from db.schemas import UrlValidator
from fastapi import FastAPI
from utils import generate_short_url

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.post("/generate_url")
def url_input(url: UrlValidator):
    url = generate_short_url(str(url))
    return {"short_url": url}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
import uvicorn
from db.schemas import UrlValidator
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from utils import hash_url, retrieve_url_by_hashed_url

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.post("/get-url")
async def retrieve_url(request: Request, hashed_url: UrlValidator) -> RedirectResponse:
    input_url = hashed_url.input_url
    url = retrieve_url_by_hashed_url(str(input_url))
    response = RedirectResponse(url=url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    return response


@app.post("/generate-url")
async def generate_hashed_url(url: UrlValidator) -> JSONResponse:
    input_url = url.input_url
    hashed_url = hash_url(str(input_url))
    response = JSONResponse(content={"hashed_url": hashed_url})
    return response


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="localhost", port=8000, reload=True)

import uvicorn
from db.schemas import UrlValidator
from fastapi import FastAPI, status, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from utils import hash_url, retrieve_url_by_hashed_url

app = FastAPI(
    title="Short URL Generator",
    version="0.0.1",
    docs_url="/api/docs",
    description="A Small Function For Generate Short URL.",
)

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/index", tags=["index"])
async def index():
    return {"message": "Hello World"}


@app.post("/retrieve-original-url", tags=["Original URL"])
async def retrieve_url(hashed_url: str = Form(...)) -> RedirectResponse:
    input_url = hashed_url
    url = retrieve_url_by_hashed_url(str(input_url))
    response = RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    return response


@app.post("/generate-short-url", tags=["Hashed URL"])
async def generate_url(url: UrlValidator) -> JSONResponse:
    input_url = url.input_url
    hashed_url = hash_url(str(input_url))
    response = JSONResponse(content={"hashed_url": hashed_url})
    return response


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="0.0.0.0", port=8000, reload=True)

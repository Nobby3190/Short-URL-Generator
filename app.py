from db.schemas import UrlValidator
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils import hashing_original_url, retrieve_url_by_hashed_url

app = FastAPI(
    title="Short URL Generator",
    version="0.0.1",
    docs_url="/urls/api/docs",
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


@app.get("/urls/{hashed_url}", tags=["URL"])
async def original_url(hashed_url: str) -> JSONResponse:
    url = retrieve_url_by_hashed_url(hashed_url)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL is not found"
        )
    elif url == "Invalid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid hashed url format"
        )
    response = JSONResponse(content={"url": url})
    return response


@app.post("/urls/generate", tags=["URL"])
async def hash_url(url: UrlValidator) -> JSONResponse:
    input_url = url.input_url
    hashed_url = hashing_original_url(input_url)
    if not hashed_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL format"
        )
    response = JSONResponse(content={"hashed_url": hashed_url})
    return response

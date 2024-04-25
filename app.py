import uvicorn
from db.schemas import UrlValidator
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse, RedirectResponse
from utils import hash_url, retrieve_url_by_hashed_url

app = FastAPI(
    title="Short URL Generator",
    version="0.0.1",
    docs_url="/api/docs",
    description="A Small Function For Generate Short URL.",
)

# origins = [
#     "*",
#     "http://localhost:8000/"
#     ]


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.post("/redirect-test")
async def login():
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/retrieve-original-url", tags=["Original URL"])
async def retrieve_url(hashed_url: UrlValidator) -> RedirectResponse:
    input_url = hashed_url.input_url
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
    uvicorn.run(app="app:app", host="127.0.0.1", port=8000, reload=True)

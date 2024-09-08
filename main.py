import os
import dotenv
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

# Load environment variables from .env file
dotenv.load_dotenv()

app = FastAPI(
    title="Hello World API",
    description="A simple API that says hello",
    version="1.0.0"
)


class HelloResponse(BaseModel):
    message: str


@app.get("/", response_model=HelloResponse)
async def root():
    """
    Root endpoint that returns a hello message.
    """
    return {"message": "Hello World"}


@app.get("/hello/{name}", response_model=HelloResponse)
async def say_hello(name: str):
    """
    Endpoint that says hello to a specific name.
    """
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    port = os.getenv("PORT", 8000)

    print("API Route: http://0.0.0.0:{}".format(port))
    print("ReDoc OpenAPI: http://0.0.0.0:{}/redoc".format(port))
    print("Swagger OpenAPI: http://0.0.0.0:{}/docs".format(port))

    uvicorn.run(app, host="0.0.0.0", port=port)

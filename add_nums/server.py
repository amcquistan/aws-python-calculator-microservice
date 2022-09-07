from uuid import uuid4

from fastapi import FastAPI
import uvicorn

from config import configure
from models import AddNumsRequest, AddNumsResponse
from services import Calculator


settings = configure()
calc = Calculator(settings)
app = FastAPI()


@app.get("/add/health")
def health():
  return "Ok"


@app.post("/add", response_model=AddNumsResponse)
def add(request: AddNumsRequest) -> float:
  """Adds numbers"""
  response = AddNumsResponse(result=calc.add(request.nums),
                        request_id=str(uuid4()))
  return response


if __name__ == '__main__':
  uvicorn.run(app, host='0.0.0.0', port=settings.port)

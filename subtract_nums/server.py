from uuid import uuid4

from fastapi import FastAPI
import uvicorn

from config import configure
from models import SubtractRequest, SubtractResponse
from services import Calculator


settings = configure()
calc = Calculator(settings)
app = FastAPI()


@app.post('/subtract', response_model=SubtractResponse)
def subtract(request: SubtractRequest) -> SubtractResponse:
  """Subtracts numbers"""
  return SubtractResponse(result=calc.subtracts(request.nums),
                  request_id=str(uuid4()))


if __name__ == '__main__':
  uvicorn.run(app, host='0.0.0.0', port=settings.port)

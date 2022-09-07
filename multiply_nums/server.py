from functools import reduce
from uuid import uuid4

from fastapi import FastAPI
import uvicorn

from config import configure
from models import MultiplyRequest, MultiplyResponse
from services import Calculator


settings = configure()
calc = Calculator(settings)
app = FastAPI()


@app.post('/multiply', response_model=MultiplyResponse)
def multiply(request: MultiplyRequest) -> MultiplyResponse:
  """Multiplies numbers"""
  return MultiplyResponse(result=calc.multiply(request.nums),
                          request_id=str(uuid4()))


if __name__ == '__main__':
  uvicorn.run(app, host='0.0.0.0', port=settings.port)

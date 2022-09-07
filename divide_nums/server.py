from uuid import uuid4
from fastapi import FastAPI
import uvicorn

from config import configure
from models import DivideRequest, DivideResponse
from services import Calculator


settings = configure()
calc = Calculator(settings)
app = FastAPI()


@app.post('/divide', response_model=DivideResponse)
def divide(request: DivideRequest) -> DivideResponse:
  """Divides numbers"""
  return DivideResponse(result=calc.divide(request.nums),
                       request_id=str(uuid4()))


if __name__ == '__main__':
  uvicorn.run(app, host='0.0.0.0', port=settings.port)

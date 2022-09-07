from uuid import uuid4
from fastapi import FastAPI
import uvicorn

from config import configure
from models import AverageRequest, AverageResponse
from services import Calculator


settings = configure()
calc = Calculator(settings)
app = FastAPI()


@app.post('/average', response_model=AverageResponse)
def average(request: AverageRequest) -> AverageResponse:
  """Averages numbers"""
  result = calc.average(request.nums)
  return AverageResponse(result=result,
                  request_id=str(uuid4()))


if __name__ == '__main__':
  uvicorn.run(app, host='0.0.0.0', port=settings.port)

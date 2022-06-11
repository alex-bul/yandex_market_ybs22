import uvicorn

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from core.error_handler import ValidationErrorResponse
from schemas.shop_unit import ShopUnitImportRequest

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return ValidationErrorResponse


@app.post("/imports",
          responses={
              400: {
                  "description": "Невалидная схема документа или входные данные не верны.",
                  "content": {
                      "application/json": {
                          "example": {"code": 400, "message": "Validation Failed"}
                      }
                  },
              }
          })
async def imports(data: ShopUnitImportRequest):
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='127.0.0.1', reload=True)

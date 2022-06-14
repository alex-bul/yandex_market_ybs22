import uvicorn

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from core.errors import validation_error_response

from db import models
from db.database import engine

from routers import shop_unit

app = FastAPI()
app.include_router(shop_unit.router, responses={
    400: {
        "description": "Невалидная схема документа или входные данные не верны.",
        "content": {
            "application/json": {
                "example": {"code": 400, "message": "Validation Failed"}
            }
        },
    }
})

models.Base.metadata.create_all(bind=engine)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # TODO убрать
    print(exc.args)
    return validation_error_response


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='127.0.0.1', reload=True)

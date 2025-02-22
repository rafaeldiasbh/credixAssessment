from fastapi import APIRouter
from ....schemas.hello import HelloMessage
from ....services.hello_service import get_hello_message
from http import HTTPStatus

router = APIRouter()

@router.get("/", status_code=HTTPStatus.OK, response_model=HelloMessage)
def read_root():
    return get_hello_message()
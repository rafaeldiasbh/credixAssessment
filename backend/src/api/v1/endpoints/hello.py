from fastapi import APIRouter
from ....schemas.hello import HelloMessage
from ....services.hello_service import get_hello_message

router = APIRouter()

@router.get("/", response_model=HelloMessage)
def read_root():
    return get_hello_message()
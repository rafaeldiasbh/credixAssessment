from ..schemas.hello import HelloMessage

def get_hello_message() -> HelloMessage:
    return HelloMessage(message="Hello World")
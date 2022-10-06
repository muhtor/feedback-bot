

class MessageException(Exception):
    ERROR_NOT_POST_REQUEST = 10
    ERROR_CAN_NOT_PARSING_JSON = 11
    ERROR_INVALID_JSON_OBJECT = 12
    ERROR_METHOD_NOT_FOUND = 13

    error = {}
    data = None
    messages = None
    exception_msg = None
    code = None

    def __init__(self, message, code, data=None):
        self.messages = message
        self.code = code
        self.data = data
        self.error = {"code": self.code}
        if self.messages:
            self.error['message'] = self.messages
            self.exception_msg = f"Error: {self.error['message']}"
        if self.data:
            self.error['data'] = self.data
            self.exception_msg = f"Error: {self.error['message']}, in {self.error['data']}"

    def message(self):
        return self.messages

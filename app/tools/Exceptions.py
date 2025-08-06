class ToolError(Exception):
    def __init__(self, message):
        self.message = message

class OpenmanusError(Exception):
    pass
class TokenLimitExceeded(OpenmanusError):
    pass
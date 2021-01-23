import pexpect
class Command():
    def __init__(command: str, arguments: list, read: str):
        self.command = command
        self.arguments = arguments
        self.read = read

class Edit():
    pass

class Slide():
    pass
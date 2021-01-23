import pexpect
class Command():
    def __init__(command: str, arguments: list):
        self.command = command
        self.arguments = arguments

    def fake_start(self, text: str) -> None:
        """To print the first command before creating a child process.

        Args:
            text (str): The command that will be used to spawn a child
            process with pexpect.

        Returns:
            None: None
        """

        letters = list(text)
        for letter in letters[0: -1]:
            print(letter, end = "", flush = True)
            time.sleep(.11) #TODO: This should be randomized.
        print(splitted[-1])

        return None

    def 

    def run(self):
        pass

class Read():
    def __init__(read: str):
        self.to_read = read
class Edit():
    pass

class Slide():
    pass
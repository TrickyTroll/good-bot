import pexpect
import sys
class Commands:
    def __init__(commands: list, expect: list):
        self.commands = commands
        self.expect = expect
        self.initial = commands[0]

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

    def fake_typing(self, text: str) -> None:
        """Fake typing of commands

        Args:
            text (str): The text to type

        Returns:
            None: None
        """
        letters = list(text)
        letters.append("\n")
        for letter in letters:
            time.sleep(.12) #TODO: This should also be random.
            child.send(things)
        
        return None
    
    def fake_typing_secret(self, secret: str) -> None:
        """To fake type a password or other secret. This ensures that the
        password won't be recorded.

        Args:
            secret (str): The secret that has to be typed

        Returns:
            None: None
        """

        child.logfile = None
        child.logfile_read = sys.stdout
        child.delaybeforesend = 1
        child.sendline(password)
        child.logfile = sys.stdout
        child.logfile_read = None

        return None

    def run(self):

class Read:
    def __init__(read: str):
        self.to_read = read
class Edit:
    pass

class Slide:
    pass
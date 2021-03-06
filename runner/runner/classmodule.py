import pexpect
import sys
import time


class Commands:
    def __init__(self, commands: list, expect: list):
        # The first command will be typed using fake_typing.
        self.initial = commands[0]
        # The other commands will be sent using send.
        self.commands = commands[1:]
        self.expect = expect
        self.dir_name = "commands"

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
            print(letter, end="", flush=True)
            time.sleep(.11)  # TODO: This should be randomized.
        print(letters[-1])

        return None

    def get_directory(self) -> str:
        """Returns the dir_name attr.

        Returns:
            str: The dir_name.
        """
        return self.dir_name

    def fake_typing(self, text: str, child: pexpect.pty_spawn.spawn) -> None:
        """Fake typing of commands

        Args:
            text (str): The text to type
            child (pexpect.pty_spawn.spawn): The child process.

        Returns:
            None: None
        """
        letters = list(text)
        letters.append("\n")
        for letter in letters:
            time.sleep(.12)  # TODO: This should also be random.
            child.send(letter)

        return None

    def fake_typing_secret(self, secret: str, child: pexpect.pty_spawn.spawn) -> None:
        """To fake type a password or other secret. This ensures that the
        password won't be recorded.

        Args:
            secret (str): The secret that has to be typed
            child (pexpect.pty_spawn.spawn): The child process.

        Returns:
            None: None
        """

        child.logfile = None
        child.logfile_read = sys.stdout
        child.delaybeforesend = 1
        child.sendline(secret)
        child.logfile = sys.stdout
        child.logfile_read = None

        return None

    def is_password(self, returning: str) -> bool:
        """Checks if the next thing to return is as password.

        Args:
            returning (str): The string that will be typed ot answer
            the prompt.

        Returns:
            bool: Wether the answer will be a password or not.
        """

        password_string = returning.split()

        if password_string[0] == "Password":

            return True

        return False

    def run(self) -> None:
        """Runs the command and anwsers all prompts for the sequence.

        Returns:
            None: None
        """
        child = pexpect.spawn("bash", echo = False)
        child.logfile = sys.stdout.buffer
        # TODO: This should be changed for a better regex 
        # (check for the EOL).
        child.expect("#")

        self.fake_typing(self.initial, child)
        for i in range(len(self.commands)):
            if self.is_password(self.commands[i]):
                # TODO: This is where the password getter shoud happen.
                print("Passwords havent been implemented yet.")
                sys.exit()
            else:
                if self.expect[i] == "prompt":
                    child.expect("#")
                else:
                    child.expect(self.expect[i])

                self.fake_typing(self.commands[i], child)

        child.expect("#")
        child.close()

        return None

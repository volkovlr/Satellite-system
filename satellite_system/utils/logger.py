from datetime import datetime
from .singleton import singleton

@singleton
class Logger:
    def __init__(self):
        """A class for logging system messages
        """
        self.log_file = "app.log"

    def write(self, type: str, message: str):
        """Printing system message and saving it in file 'app.log'

        Args:
            type (str)
            message (str)
        """
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = f"[{time}] [{type}] {message}"

        if (type != "INFO"):
            print(message)

        with open(self.log_file, "a") as f:
            f.write(message + "\n")

    def info(self, message: str):
        """printing and saving "info" messages

        Args:
            message (str)
        """
        self.write("INFO", message)

    def error(self, message: str):
        """printing and saving "error" messages

        Args:
            message (str)
        """
        self.write("ERROR", message)

    def result(self, message: str):
        """printing and saving "result" messages

        Args:
            message (str)
        """
        self.write("RESULT", message)

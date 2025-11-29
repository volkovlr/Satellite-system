from datetime import datetime
from singleton import singleton

@singleton
class Logger:
    def __init__(self):
        self.log_file = "app.log"

    def write(self, type: str, message: str):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = f"[{time}] [{type}] {message}"

        if (type is not "INFO"):
            print(message)

        with open(self.log_file, "a") as f:
            f.write(message + "\n")

    def info(self, message: str):
        self.write("INFO", message)

    def error(self, message: str):
        self.write("ERROR", message)

    def result(self, message: str):
      self.write("RESULT", message)

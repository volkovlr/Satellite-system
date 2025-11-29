from command_proc import CommandProcessor
from utils.logger import Logger

class Main:
    def __init__(self):
        self.logger = Logger("MAIN")
        self.processor = CommandProcessor()

    def handle_input(self, input_line: str):
        self.logger.info(f"USER INPUT: {input_line}")
        try:
            self.processor.execute(input_line)

        except Exception as e:
            self.logger.error(f"ERROR: {e}")

    def run(self):
        print("Enter the command\n")

        while True:
            user_input = input()
            if not user_input:
                continue

            if user_input == "exit":
                self.logger.info("The work is completed")
                break

            self.handle_input(user_input)

if __name__ == "__main__":
    Main().run()

from .command_proc import CommandProcessor
from satellite_system.utils.logger import Logger

class Main:
    def __init__(self):
        self.logger = Logger()
        self.processor = CommandProcessor()

    def run(self):
        print("Enter the command\n")

        while True:
            user_input = input()
            if not user_input:
                continue

            if user_input == "exit":
                self.logger.info("The work is completed")
                break

            self.logger.info(f"USER INPUT: {user_input}")

            try:
                self.processor.execute(user_input)

            except Exception as e:
                self.logger.error(e)
                break

if __name__ == "__main__":
    Main().run()

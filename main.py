from storage import storage
from exceptions import ExitProgram
from command_handler import execute_command
from importlib import import_module

import_module('contacts_commands')
import_module('notes_commands')


def parse_input(user_input):
    try:
        cmd, *args = user_input.split()
    except:
        return "Invalid command."
    cmd = cmd.strip().lower()
    return cmd, *args


def start_bot():
    print_welcome()
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        try:
            print(execute_command(command, args))
        except ExitProgram as e:
            print(str(e))
            break


def print_welcome():
    try:
        with open("data/welcome.txt", 'r') as f:
            print(f.read())
    except:
        pass
    finally:
        print("Welcome to the C4 Assistant Bot! Type 'help' for reference.")


def main():
    with storage:
        start_bot()


if __name__ == "__main__":
    main()

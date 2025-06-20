import sys

prompt: str = r"\>> "

def take_user_input():
    try:
        _user_input = input(prompt).strip()
    except KeyboardInterrupt:
        print("Exiting program...\n")
        sys.exit(0)
    except EOFError:
        print("Exiting program...\n")
        sys.exit(0)
    return _user_input

def exit_program(user_input: str) -> None:
    if user_input.lower() == "exit" or user_input.lower() == "quit" or user_input.lower() == "q":
        print("Exiting program...")
        sys.exit(0)
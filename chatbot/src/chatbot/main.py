from .utils.terminal import exit_program, take_user_input


def welcome_bot_drawing():
    bot_art = r"""
       _______
     /         \
    |  Hello!   |
     \_______  /
             \|
        .-""""""-.
       / -   -   \\
      |  o   o    |
      |    ^      |
       \  '-'   _/
        '-.__.-'
    """
    print(bot_art)
    print("Hello how can I help you?\n")


def main():
    __welcome_message = False
    while True:
        if not __welcome_message:
            __welcome_message = not __welcome_message
            welcome_bot_drawing()
            user_input = take_user_input()
            exit_program(user_input)
        else:
            user_input = take_user_input()
            exit_program(user_input)
        
        print(user_input)
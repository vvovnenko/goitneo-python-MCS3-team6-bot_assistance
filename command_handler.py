import functools
import types
from exceptions import ValidationException, BotSyntaxException, \
    DuplicateException, NotFoundException, ExitProgram, InvalidCommandError
from util.string_utils import get_similarity_score

COMMANDS = dict[str, types.FunctionType]()


def create_invalid_command_response(command: str) -> str:
    guessed_command = find_similar_command(command)
    response = f"'{command}' is not a bot-helper command. See 'help'."
    if guessed_command:
        response += "\n    " + f"did you mean {guessed_command} ?"
    return response


def find_similar_command(command: str) -> str:
    similar_commands = dict()
    for guessed_command in COMMANDS.keys():
        score = get_similarity_score(command, guessed_command)
        if score > 0:
            similar_commands[guessed_command] = score

    if not similar_commands:
        return None

    max_score = max(similar_commands.values())
    guessed_commands = [f"'{k}'" for k, v in similar_commands.items() if v == max_score]
    return " or ".join(guessed_commands)


def create_command_doc(command_name: str) -> str:
    command = COMMANDS.get(command_name, None)
    if command is None:
        return create_invalid_command_response(command_name)
    else:
        return command.__doc__


def create_command_description(command_name: str) -> str:
    command = COMMANDS.get(command_name, None)
    if command is None:
        return ''
    else:
        return command.__doc__.split('\n')[0] if command.__doc__ else '-'


def get_handler(command: str):
    handler = COMMANDS.get(command)
    if handler is None:
        raise InvalidCommandError('Invalid command.')
    return handler


def command(name):
    """Register a function as a plug-in"""

    def register_command(func):
        COMMANDS[name] = func
        return func

    return register_command


def input_error(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValidationException, DuplicateException, NotFoundException) as e:
            return e
        except BotSyntaxException as e:
            return e

    return inner


@command(name='hello')
def hello(args) -> str:
    '''Just greet youself'''
    return 'How can I help you?'


@command(name='exit')
@command(name='close')
def exit(*args, **kwargs):
    '''Exit from assistant'''
    raise ExitProgram('Good bye!')


@command(name='help')
def help(args):
    """Show info about all commands
    usage:
        help [command_name]
    arguments:
        command_name - name of the comand (optional)
    """
    if len(args) > 0:
        return '\n' + create_command_doc(args[0])

    lines = []
    for command in COMMANDS.keys():
        lines.append('{:<20}:\t{}'.format(command, create_command_description(command)))
    return '\n'.join(lines)


@input_error
def execute_command(command: str, args: list[str]):
    try:
        return get_handler(command)(args)
    except InvalidCommandError:
        return create_invalid_command_response(command)
    except (BotSyntaxException, TypeError, ValueError, KeyError):
        return f'Command syntax error. Run "help {command}"'

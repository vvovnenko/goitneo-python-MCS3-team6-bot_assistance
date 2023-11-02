import functools
import types
from exceptions import ValidationException, BotSyntaxException, DuplicateException, NotFoundException, ExitProgram, InvalidCommandError

COMMANDS = dict[str, types.FunctionType]()

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
    '''Show info about all commands'''
    lines = []
    for command, func in COMMANDS.items():
        lines.append('{:<20}:\t{}'.format(command, func.__doc__))
    return '\n'.join(lines)

@input_error
def execute_command(command: str, args: list[str]):
    try:
        return get_handler(command)(args)
    except InvalidCommandError:
        return 'Unknown command'
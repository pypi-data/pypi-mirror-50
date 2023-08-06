import time

COMMANDS = { }

def _help():
    """Print help info about commands"""
    for fname, f in COMMANDS.items():
        docstr = f.__doc__
        info = fname
        if docstr:
            info += ':\t' + docstr
        print(info)

COMMANDS['help'] = _help

def command(func):
    """Just a decorator for `add_func()`"""
    add_command(func)
    return func

def add_command(func):
    """
    Add a command to the cli.

    Use help to list all commands
    """
    global COMMANDS
    COMMANDS[func.__name__] = func

def start():
    """
    Starts the interactive cli
    """
    try:
        input_loop()
    except KeyboardInterrupt:
        print("Bye")
        return
    except EOFError:
        print("Done")
        return
# Input-related methods
# --------
def parse_command(comm):
    """
    Parse a string to command name and arguments.

    :param comm: A string consisting 1 or more words separated by spaces and an optional json as the last word 
    :return: 2-tuple: command name, args list
    """
    # Just perform a command without args
    if ' ' not in comm:
        return comm, []
    else:
        words = comm.split(' ')
        words = [w for w in words if w is not '']
        method_name = words.pop(0)
        return method_name, words

def input_loop():
    """
    This runs in a thread and polls input, then parses
    arguments and executes method.
    Prints to stderr if there was an error
    """
    while True:
        command = input()
        method_name, args = parse_command(command)
        method = COMMANDS.get(method_name)
        if method is None:
            print(f"Command `{method_name}` not found. Type help to display available commands.")
            continue
        try:
            method( *args )
        except Exception as e:
            print("Error executing:", str(e))
        time.sleep(0)

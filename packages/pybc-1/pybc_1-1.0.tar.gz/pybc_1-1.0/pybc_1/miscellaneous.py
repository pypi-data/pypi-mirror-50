"""This module implements unix command 'exit','date','hostname',
'whoami','history','timeit' in python.
"""
import sys
import time
import getpass
import socket
from importlib import import_module
DIRECTORY_COMMANDS = ["ls", "mkdir", "pwd", "rmdir", "cd"]
FILE_COMMANDS = ["cat", "cp", "rm", "mv", "grep", "head", "tail", "sizeof", "find"]
def __help_exit():
    """Function gives description and usage about 'exit' command
    """
    print("Description: This exits the PyShell.")
    print("Usage: exit")
def __help_date():
    """Function gives description and usage about 'date' command
    """
    print("Description: This prints the current date and time.")
    print("Usage: date")
def __help_hostname():
    """Function gives description and usage about 'hostname' command
    """
    print("Description: This prints hostname.")
    print("Usage: hostname")
def __help_whoami():
    """Function gives description and usage about 'whoami' command
    """
    print("Description: This prints user name.")
    print("Usage: whoami")
def __help_history():
    """Function gives description and usage about 'history' command
    """
    print("Description: This prints history of all the commands.")
    print("Usage: history")
def __help_timeit():
    """Function gives description and usage about 'timeit' command
    """
    print("Description: This prints the time taken for a command run.")
    print("Usage: timeit")
def exit_pyshell(command):
    """Function implementing 'exit' command.
    """
    command = command.strip()
    list_exit = [True]
    if "-h" in command or "--help" in command:
        __help_exit()
        return list_exit
    print("Exiting PyShell.")
    sys.exit()
def date(command):
    """Function implementing 'date' command.
    """
    list_date = [True]
    if "-h" in command or "--help" in command:
        __help_date()
        return list_date
    list_date.insert(1, time.strftime("%a %b  %d %H:%M:%S IST %Y"))
    print(list_date[1])
    return list_date

def hostname(command):
    """Function implementing 'hostname' command.
    """
    list_hostname = [True]
    if "-h" in command or "--help" in command:
        __help_hostname()
        return list_hostname
    list_hostname.insert(1, socket.gethostname())
    print(list_hostname[1])
    return list_hostname

def whoami(command):
    """Function implementing 'whoami' command.
    """
    list_whoami = [True]
    if "-h" in command or "--help" in command:
        __help_whoami()
        return list_whoami
    list_whoami.insert(1, getpass.getuser())
    print(list_whoami[1])
    return list_whoami

def history_pyshell(command):
    """Function implementing 'history' command.
    """
    list_history = [True]
    if "-h" in command or "--help" in command:
        __help_history()
        return list_history
    with open("log.txt", "r") as history_file:
        for i, line in enumerate(history_file):
            print(i + 1, line.strip())
    return list_history
MIS_FUNCTIONS = {"date":date, "whoami":whoami, "hostname":hostname, "exit":exit_pyshell,\
"history": history_pyshell}
def timeit(command):
    """Function implementing 'timeit' command.
    """
    list_timeit = [True]
    try:
        if "-h" in command or "--help" in command:
            __help_timeit()
            return list_timeit
        flag = 1
        command = command.split()
        module_name = command[1]
        command = "".join(command[1:])
        if module_name in DIRECTORY_COMMANDS:
            folder = "directory"
        elif module_name in FILE_COMMANDS:
            folder = "files"
        else:
            flag = 0
            folder = ""
        if flag == 1:
            start_time = time.time()
            import_module(f"{folder}.{module_name}").run(command)
            time_taken = time.time() - start_time
        else:
            start_time = time.time()
            MIS_FUNCTIONS[module_name](command)
            time_taken = time.time() - start_time
        list_timeit.insert(1, time_taken)
        print(f"'{command}' took {time_taken} seconds.")
        return list_timeit
    except:
        print("Invalid usage.")
        __help_timeit()
        return [False]

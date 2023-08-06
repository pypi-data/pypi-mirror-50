"""This module mimics the UNIX command prompt.
"""
from importlib import import_module
from help import ___help
import rlcompleter
import subprocess
import sys
import os
import miscellaneous as mis
MISCOMMANDS = {"date":mis.date, "whoami":mis.whoami, "hostname":mis.hostname,\
"timeit":mis.timeit, "exit":mis.exit_pyshell, "history": mis.history_pyshell}
DIRCOMMANDS = ["ls", "mkdir", "pwd", "rmdir", "cd"]
FILECOMMANDS = ["cat", "cp", "rm", "mv", "grep", "head", "tail", "sizeof", "find"]
def and_fun(command):
    """Function implementing logical And of commands.
    """
    for com in command:
        if not execute(com):
            break
    return True
def or_fun(command):
    """Function implementing logical Or of commands.
    """
    for com in command:
        if execute(com):
            break
    return True
JOINTS = {"&&": and_fun, "||": or_fun}
def execute(command):
    """Function tokenizes and executes the command.
    """
    flag = 0
    for i in JOINTS:
        if i in command:
            flag = 1
            command = command.strip().split(f"{i}")
            JOINTS[i](command)
    if flag == 0:
        response = True
        module_name = command.split()[0]
        try:
            if module_name in MISCOMMANDS.keys():
                response = MISCOMMANDS[module_name](command)[0]
            else:
                if module_name in DIRCOMMANDS:
                    folder = "directory"
                elif module_name in FILECOMMANDS:
                    folder = "files"
                try:
                    module_parsed = import_module(f"{folder}.{module_name}")
                    response = module_parsed.run(command)[0]
                except UnboundLocalError:
                    print(f"'{module_name}' is an invalid command.")
            return response
        except ModuleNotFoundError:
            print(f"'{module_name}' is an invalid command.")
    return True
def __main__():
    logPath = os.getcwd()
    while True:
        try:
            command = input("PyShell> ")
            if command == "":
                continue
            if command == "break":
                break
            if command == "help":
                ___help()
                return
        except KeyboardInterrupt:
            break
        with open(f"{logPath}\log.txt", "a") as history:
            print(command, file=history)
        command = command.strip().split(";")
        for cmd in command:
            execute(cmd)
__main__()
        

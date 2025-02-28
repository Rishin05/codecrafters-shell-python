import sys
import shutil
import subprocess
import os
import shlex

BUILTIN_CMD = {"exit", "echo", "type","pwd","cd"}

def type_cmd(command):
    if command in BUILTIN_CMD:
        print(f"{command} is a shell builtin")
    elif (path := shutil.which(command)):
        print(f"{command} is {path}")
    else:
        print(f"{command}: not found")

def run_external_command(command_parts):
    """Runs an external program if found in PATH."""
    try:
        subprocess.run(command_parts)
    except FileNotFoundError:
        print(f"{command_parts[0]}: command not found")
    except PermissionError:
        print(f"{command_parts[0]}: permission denied")


def change_directory(path):
    """Handles changing the directory, supporting absolute, relative, and ~ paths."""
    try:
        # Handle '~' and '~/something'
        if path == "~" or path.startswith("~/"):
            path = os.path.expanduser(path)  # Expands to the home directory

        # Resolve absolute or relative path
        target_path = os.path.abspath(path) if not os.path.isabs(path) else path
        os.chdir(target_path)  # Change directory
    except FileNotFoundError:
        print(f"cd: no such file or directory: {path}")
    except PermissionError:
        print(f"cd: permission denied: {path}")

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command_parts = shlex.split(input()) # Split the input into parts using shlex let that be single double backslash qouted executable

        if not command_parts:
            continue  # Skip empty input

        command = command_parts[0]
        args = command_parts[1:]

        if command == "exit" and args == ["0"]:
            exit()
        elif command == "echo":
            print(" ".join(args))
        elif command == "type" and len(args) == 1:
            type_cmd(args[0])
        elif command == "pwd":
            print(os.getcwd())
        elif command == "cd" and len(args) == 1:
            change_directory(args[0])
        elif shutil.which(command):
            run_external_command(command_parts)
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()

import sys
import shutil
import subprocess
import os

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

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command_parts = input().split()

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
            if os.path.isabs(args[0]): 
                try:
                    os.chdir(args[0]) 
                except FileNotFoundError:
                    print(f"cd: no such file or directory: {args[0]}")
                except PermissionError:
                    print(f"cd: permission denied: {args[0]}")
        elif shutil.which(command):
            run_external_command(command_parts)
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()

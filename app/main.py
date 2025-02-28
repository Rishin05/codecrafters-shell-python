import sys
import shutil
import subprocess
import os

BUILTIN_CMD = {"exit", "echo", "type", "pwd", "cd"}

def type_cmd(command):
    if command in BUILTIN_CMD:
        print(f"{command} is a shell builtin")
    elif (path := shutil.which(command)):
        print(f"{command} is {path}")
    else:
        print(f"{command}: not found")

def run_external_command(command_parts, output_file=None):
    """Runs an external program, optionally redirecting output to a file."""
    try:
        with open(output_file, "w") if output_file else sys.stdout as f:
            subprocess.run(command_parts, stdout=f, text=True, check=True)
    except FileNotFoundError:
        print(f"{command_parts[0]}: command not found")
    except PermissionError:
        print(f"{command_parts[0]}: permission denied")
    except subprocess.CalledProcessError:
        print(f"{command_parts[0]}: command failed")

def change_directory(path):
    """Handles changing the directory, supporting absolute, relative, and ~ paths."""
    try:
        if path == "~" or path.startswith("~/"):
            path = os.path.expanduser(path)  # Expands to the home directory
        os.chdir(path)
    except FileNotFoundError:
        print(f"cd: no such file or directory: {path}")
    except PermissionError:
        print(f"cd: permission denied: {path}")

def parse_command(input_line):
    """Parses the command line input and handles output redirection."""
    parts = input_line.split()
    if ">" in parts:
        idx = parts.index(">")
        command_parts = parts[:idx]
        output_file = parts[idx + 1] if idx + 1 < len(parts) else None
        return command_parts, output_file
    return parts, None

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        input_line = input().strip()

        if not input_line:
            continue  # Skip empty input

        command_parts, output_file = parse_command(input_line)
        if not command_parts:
            continue

        command = command_parts[0]
        args = command_parts[1:]

        if command == "exit" and args == ["0"]:
            exit()
        elif command == "echo":
            output = " ".join(args)
            if output_file:
                with open(output_file, "w") as f:
                    f.write(output + "\n")
            else:
                print(output)
        elif command == "type" and len(args) == 1:
            type_cmd(args[0])
        elif command == "pwd":
            output = os.getcwd()
            if output_file:
                with open(output_file, "w") as f:
                    f.write(output + "\n")
            else:
                print(output)
        elif command == "cd" and len(args) == 1:
            change_directory(args[0])
        elif shutil.which(command):
            run_external_command(command_parts, output_file)
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()

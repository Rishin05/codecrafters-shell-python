import sys
import shutil

BUILTIN_CMD = {"exit", "echo", "type"}

def type_cmd(command):
    if command in BUILTIN_CMD:
        print(f"{command} is a shell builtin")
    elif (path := shutil.which(command)):
        print(f"{command} is {path}")
    else:
        print(f"{command}: not found")

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input().split()

        if not command:
            continue  # Skip empty input

        if command[0] == "exit" and len(command) == 2 and command[1] == "0":
            exit()
        elif command[0] == "echo":
            print(" ".join(command[1:]))
        elif command[0] == "type" and len(command) == 2:
            type_cmd(command[1])
        else:
            print(f"{command[0]}: command not found")

if __name__ == "__main__":
    main()

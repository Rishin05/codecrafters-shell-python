import sys


def main():
    # Uncomment this block to pass the first stage
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit 0":
            sys.exit(0)
        if command.startswith("echo "):
            print(command[5:])
        elif command.startswith("type "):
            cmd_name = command[5:]
            if cmd_name in {"echo", "exit","type"}:
                print(f"{cmd_name} is a shell builtin")
            else:
                print(f"{cmd_name}: not found")
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()

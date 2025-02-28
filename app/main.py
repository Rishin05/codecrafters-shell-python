import sys
import shutil
import subprocess
import os
import shlex
import readline
import glob

bic = ['echo', 'exit', 'cd', 'pwd', 'type']
cn = 0
history = []  # Store previous words for `echo`

def gex():
    paths = os.environ.get("PATH", "").split(os.pathsep)
    execs = set()
    for p in paths:
        if os.path.isdir(p):
            for f in os.listdir(p):
                fp = os.path.join(p, f)
                if os.access(fp, os.X_OK):
                    execs.add(f)
    return execs

def autoc(text, state):
    global cn
    
    buffer = readline.get_line_buffer()
    words = buffer.split()

    if len(words) == 0:  # No input yet
        options = sorted(bic + list(gex()))
    elif len(words) == 1:  # Completing a command
        options = sorted(cmd for cmd in bic + list(gex()) if cmd.startswith(text))
    else:  # Completing arguments
        cmd = words[0]
        if cmd == "cd":  # Suggest directories for 'cd'
            options = sorted(d + "/" for d in os.listdir() if os.path.isdir(d) and d.startswith(text))
        elif cmd == "echo":  # Suggest previous words for 'echo'
            options = sorted(set(history))  # Avoid repeating words
        elif cmd == "type":  # Suggest commands for 'type'
            options = sorted(bic + list(gex()))
        elif text.startswith(("./", "../", "/")):  # File completion
            options = glob.glob(text + "*")
        else:
            options = []  # No specific completion

    if not options:
        return None
    
    if state < len(options):
        return options[state]
    
    return None

readline.parse_and_bind("tab: complete")
readline.set_completer(autoc)

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input()
        argv = shlex.split(command)

        if not argv:
            continue

        history.extend(argv[1:])  # Store arguments for history-based completion

        if ">" in argv or "1>" in argv:
            rin = argv.index('>') if '>' in argv else argv.index('1>')
            opfl = argv[rin + 1]
            argv = argv[:rin]
            with open(opfl, "w") as file:
                subprocess.run(argv, stdout=file, stderr=sys.stderr)
            continue

        elif '2>' in argv:
            rin = argv.index("2>")
            opfl = argv[rin + 1]
            argv = argv[:rin]
            with open(opfl, "w") as file:
                subprocess.run(argv, stderr=file)
            continue

        elif '1>>' in argv or '>>' in argv:
            rin = argv.index('>>') if '>>' in argv else argv.index('1>>')
            opfl = argv[rin + 1]
            argv = argv[:rin]
            with open(opfl, "a") as file:
                subprocess.run(argv, stdout=file, stderr=sys.stderr)

        elif '2>>' in argv:
            rin = argv.index("2>>")
            opfl = argv[rin + 1]
            argv = argv[:rin]
            with open(opfl, "a") as file:
                subprocess.run(argv, stderr=file)
            continue

        elif path := shutil.which(argv[0]):
            subprocess.run(argv)

        elif argv[0] == "cd":
            path = os.path.expanduser(argv[1])
            if os.path.isdir(path):
                os.chdir(path)
            else:
                print(f"cd: {path}: No such file or directory")

        elif argv[0] == "pwd":
            print(os.getcwd())

        elif argv[0] == "type":
            if argv[1] in bic:
                print(f"{argv[1]} is a shell builtin")
            elif path := shutil.which(argv[1]):
                print(f"{argv[1]} is {path}")
            else:
                print(f"{argv[1]}: not found")

        elif argv[0] == "exit":
            exit(int(argv[1]) if len(argv) > 1 else 0)

        elif argv[0] == "echo":
            print(" ".join(argv[1:]))

        else:
            print(f"{argv[0]}: command not found")

if __name__ == "__main__":
    main()
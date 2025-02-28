import sys
import shutil
import subprocess
import os
import shlex #for splitting the command line into tokens (the best)
import readline

bic = ['echo ', 'exit ', 'cd ', 'pwd ', 'type ']
cn = 0

def gex ():
    paths = os.environ.get("PATH"," ").split(os.pathsep)
    execs = set()
    for p in paths:
        if os.path.isdir(p):
            for f in os.listdir(p):
                fp = os.path.join (p,f)
                if os.access(fp, os.X_OK):
                    execs.add(f + " ")
    return execs

def lcp(str):
    if not str:
        return ""
    pre = str[0]
    for s in str[1:]:
        while not s.startswith(pre):
            pre = pre[:-1]
            if not pre:
                return ""
    return pre

def autoc (text, state):
    global cn
    nt = 1
    cs = list(set(bic + list(gex())))
    ms = sorted([cmd for cmd in cs if cmd.startswith(text)])
    
    if not ms:
        return None
    lon = lcp(ms)
    if state == 0:
        
        if lon and lon!=text:
            return lon
        elif len(ms)==1:
            return ms[0]
        else:
            sys.stdout.write("\a")
            sys.stdout.flush()
            cn = 1
            
        
        
    elif cn == 1:
        if len(ms) > 1:
            print ("\n" + " ".join(ms))
            sys.stdout.write("$ " + text)
            sys.stdout.flush()
            cn = 0
        return None
    if len(ms)==1:
        return ms[state]
    elif len(ms)> 1:
        if lon and lon!=text:
            return ms[state]
        else:
            return text
    else:
        return 
    
    #return ms[state] if len(ms)== 1  else text       
    

#readline.set_completion_display_matches_hook(display_matches)    
readline.parse_and_bind("tab: complete")
readline.set_completer(autoc)

def main():
    # Uncomment this block to pass the first stage
    while True:
        sys.stdout.write("$ ")
        #sys.stdout.flush()

    # Wait for user input
        command  = input()
        argv = shlex.split(command)
        if ">" in argv or "1>" in argv:
            if '>' in argv:
                rin = argv.index('>')
                
            else:
                rin = argv.index('1>')
                
            opfl = argv[rin + 1]
            argv = argv[:rin]
            with open (opfl,"w") as file:
                subprocess.run(argv, stdout=file, stderr=sys.stderr)
            continue
        
        
        
        elif '2>' in argv:
            rin = argv.index("2>")
            opfl = argv[rin + 1]
            argv = argv[:rin]
            
            with open (opfl,"w") as file:
                subprocess.run (argv, stderr=file)
                continue
            
            
            
        elif '1>>' in argv or '>>' in argv:
            if '>>' in argv:
                rin = argv.index('>>')
                
            else:
                rin = argv.index('1>>')
                
            opfl = argv[rin + 1]
            argv = argv[:rin]
            with open (opfl,"a") as file:
                subprocess.run(argv, stdout=file, stderr=sys.stderr)
          
          
                
        elif '2>>' in argv:
            rin = argv.index("2>>")
            opfl = argv[rin + 1]
            argv = argv[:rin]
    
            with open (opfl,"a") as file:
                subprocess.run (argv, stderr=file)
                continue
        
        
        
        elif path := shutil.which(argv[0]):
            subprocess.run(argv)
        
        
            
        elif argv[0] == "cd":
            path = argv[1]
            path = os.path.expanduser(path)
            if os.path.isdir(path):
                os.chdir(path)
            else:
                print(f"cd: {path}: No such file or directory")
        
        
            
        elif argv[0]== "pwd":
            print (f"{os.getcwd()}")
        
        
            
        elif argv[0] == "type":
            if argv[1]=="exit" or argv[1]=="echo" or argv[1]=="type" or argv[1]=="pwd" or argv[1]=="cd" :
                print (f"{argv[1]} is a shell builtin")
            elif path := shutil.which(argv[1]):
                print(f"{command[5:]} is {path}")
            else:
                print(f"{command[5:]}: not found")
        
        
                
        elif argv[0] == "exit":
            exit(int(argv[1]))
        
        
            
        elif argv[0] == "echo":
            print (" ".join(argv[1:]))
            #print(command[7:-2:])
        
        
            
        else:
            print(f"{command}: command not found")
    


if __name__ == "__main__":
    main()
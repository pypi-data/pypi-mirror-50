from os import system as cmd
import ctypes, os
from platform import system as name
from threading import Thread

#By Thiago Piassi Bonfogo

def system_name(): return name()

def check_privileges():
    try: return os.getuid() == 0
    except(AttributeError):return ctypes.windll.shell32.IsUserAnAdmin() != 0

def install_dependencies(*libs):
    if check_privileges():
        for a in range(0,len(libs)):
            if(name() == 'Windows'):cmd(f"py -m pip install {libs[a]}")
            else:cmd(f" sudo python3 -m pip install {libs[a]}")
    else:
        print("Run this script as an administrator!")

def readFile(name,flag): return open(name,flag).read()

def writeFile(data,name,flag): open(name,flag).write(data)

def clear():
    if name() == "Windows": cmd("cls")
    else: cmd("clear")

def applyToList(var,func,final_index = ""):
    if(final_index == ""):
        for a in range(0,len(var)):var[a] = func(var[a])
    else:
        for a in range(0, final_index):var[a] = func(var[a])
    return var

def getInt(msg = ""): return int(input(msg))

def getFloat(msg = ""): return  float(input(msg))

def getBytes(msg = ""): return input(msg).encode()

def average(*numbers):
    numbers = list(numbers)
    for a in range(1,len(numbers)): numbers[0] += numbers[a]
    return numbers[0]/len(numbers)

def new_thread(function,*function_args): return Thread(target=function,args=function_args)

def shell(command):cmd(command)
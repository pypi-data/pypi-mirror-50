"""
iostream is useful in C++,but we can use print() in Python.
So do not use this module
"""
__author__="CubieLee"

import time
import os
import win32api
import threading
import random

def slowsay(string,spw=0.025):
    "Print a string on the screen slowly"
    for i in string:
        print(i,end="")
        time.sleep(spw)

def cout(*args):
    "Simple function, type ',' as '<<'"
    for i in args:
        print(i,end="")

def cin(nums=True):
    "This function can get data like 1 1 1 1 1 and return a list"
    r=input()
    r=r.split()
    if(nums):
        for i in range(len(r)):
            r[i]=int(r[i])
    return r

class Controller:
    "Use this to shutdown or reboot the computer"
    def shutdown(self,sec=30):
        "Shutdown the computer in sec seconds"
        os.system("shutdown -s -t %d" % sec)
    def reboot(self,sec=30):
        "Reboot the computer in sec seconds"
        os.system("shutdown -r -t %d" % sec)
    def cancel(self):
        "Cancel the options"
        os.system("shutdown -a")

def pop(title,content):
    "Pop out a window"
    method_list = [16,64,48,5,2097152]
    win32api.MessageBox(0,content,title,random.choice(method_list))

def windows(title,content):
    "Continually pop out windows using threads"
    while True:
        thread=threading.Thread(target=pop,args=[title,content])
        thread.start()
        time.sleep(0.2)


    
    



    
    

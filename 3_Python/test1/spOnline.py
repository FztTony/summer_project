from . import sp, fc, teamHot
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import threading
import time

projectPath = "C:/Pytest/test1/"
infodir = projectPath + "Info/"



class RunThread(threading.Thread):
    def run(self):
        try:
            with open(infodir + "spState.txt", 'r', encoding='utf-8') as f:
                if f.readline() == "running\n":
                    print("ret 0")
                    return 0
        except:
            print("can't open")
        with open(infodir + "spState.txt", 'w', encoding='utf-8') as f:
            f.write("running\n")
            print("write ok")
        print(sp.main(), "sp")
        with open(infodir + "spState.txt", 'r', encoding='utf-8') as f:
            k = f.read()
            if k != "running\n":
                print("ret 1 ", [k])
                return 1
        print(fc.main(), "fc")
        with open(infodir + "spState.txt", 'r', encoding='utf-8') as f:
            k = f.read()
            if k != "running\n":
                print("ret 2 ", [k])
                return 2
        print(teamHot.main(), "hot")
        with open(infodir + "spState.txt", 'r', encoding='utf-8') as f:
            k = f.read()
            if k != "running\n":
                print("ret 3 ", [k])
                return 3
        with open(infodir + "spState.txt", 'w', encoding='utf-8') as f:
            f.write("stopped\n")
            print("ret 4")
            return 4

@csrf_exempt
def run(request):
    print("run")
    context = base()
    print(context)
    if (not context['isRunning']):
        th = RunThread()
        th.start()
    time.sleep(0.01)
    return render(request, "spOnline.html", base(False))

def base(stop = False):
    print("base")
    try:
        with open(infodir + "spState.txt",'r',encoding='utf-8') as f:
            isRunning = f.readline().strip('\n') != 'stopped'
    except:
        isRunning = False
    if (isRunning and stop):
        with open(infodir + "spState.txt",'w',encoding='utf-8') as f:
            f.write("stopped\n")
    info = []
    info.append(myGetLine("sp", 1))
    info.append(myGetLine("sp", 2))
    info.append(myGetLine("sp", 0))
    info.append(myGetLine("hot", 0))
    return {'info': info, 'isRunning': isRunning}

@csrf_exempt
def show(request):
    print("show")
    return render(request, "spOnline.html", base(True))

def myGetLine(name, lineNum, path=infodir, tail=".txt"):
    try:
        with open(path + name + tail,'r', encoding='utf-8') as f:
            list = f.readlines()
            return list[lineNum].strip('\n')
    except Exception as e:
        print(type(e))
        return "running..."

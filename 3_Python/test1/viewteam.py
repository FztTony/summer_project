# -*- coding: UTF-8 –*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import view

projectPath = "C:/Pytest/test1/"
dir = projectPath + "NewsOrigin/"
tableDir = projectPath + "TeamTable/"
newsIndexDir = projectPath + "TeamNews/"
infoDir = projectPath + "Info/"

def teamHome(request):
    table = []
    try:
        with open(infoDir + "hot.txt",encoding='utf-8') as f:
            f.readline()
            dict = eval(f.read())
            print(dict)
            sort_list = sorted(dict.items(),key=lambda d:d[1],reverse=True)
            table = [[i,j[0],j[1]] for i,j in zip(range(1,len(sort_list)+1),sort_list)]
            print(table)
    except:
        print("No Info/hot.txt")
    return render(request,"team.html",{'table':table})

def team(request, teamname, num = '1'):
    ind = []
    try:
        with open(newsIndexDir + teamname + ".txt", encoding='utf-8') as f:
            line = f.readline()
            line = line.strip('\n')
            line = line.strip(' ')
            ind = line.split(' ')
            ind.reverse()
    except:
        print("No News")
    context = view.context_base(ind,[teamname],int(num))

    context['name'] = teamname
    try:
        with open(tableDir + teamname + ".txt", encoding='utf-8') as f:
            context['fullname'] = f.readline().strip('\n')
            context['header'] = f.readline().strip('\n').split('\t')
            context['table'] = [x.split('\t') for x in f.read().strip('\n').split('\n')]
            pass
    except:
        print("No Table")

    print(context['name'])
    return render(request,"teamPage.html", context)
# -*- coding: UTF-8 –*-
import jieba
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from jieba import analyse as anls
from . import dealRepeat
import functools
import time

projectPath = "C:/Pytest/test1/"
dir = projectPath + "NewsOrigin/"
fcDir = projectPath + "NewsFC/"
infodir = projectPath + "Info/"


def cmp_for_search_base(a, b):
    if a[1] < b[1]:
        return 1
    elif a[1] > b[1]:
        return -1
    else:
        if a[0] < b[0]:
            return 1
        elif a[0] > b[0]:
            return -1
        else:
            return 0


def context_base(tar, ws, a):
    context = {}
    context['sum'] = len(tar)
    if len(tar) > a * 20:
        tar = tar[(a - 1) * 20:a * 20]
        context['hasnext'] = True
        context['next'] = a + 1
    else:
        tar = tar[(a - 1) * 20:len(tar)]
        context['hasnext'] = False
    res_list = m_render(tar, ws)
    context['res'] = res_list
    context['prev'] = a - 1
    # print(tar)
    return context


def search_mult(ws, a):
    #print("search_mult")
    #print(ws)
    dic = {}
    for w in ws:
        try:
            with open(fcDir + w + ".txt", encoding='utf-8') as f:
                line = f.readline()
                line = line.strip('\n')
                line = line.strip(' ')
                ind = line.split(' ')
                for i in ind:
                    if i in dic:
                        dic[i] = dic[i] + 1
                    else:
                        dic[i] = 1
        except:
            pass
    dict = sorted(dic.items(), key=functools.cmp_to_key(cmp_for_search_base))
    # print(dict)
    tar = [i[0] for i in dict]
    return (tar, ws)

def search_base(ws, a):
    #print("search_base")
    #print(ws)
    if len(ws) == 1:
        try:
            with open(fcDir + ws[0] + ".txt", encoding='utf-8') as f:
                line = f.readline()
                line = line.strip('\n')
                line = line.strip(' ')
                ind = line.split(' ')
                ind.reverse()
                return (ind, ws)
        except:
            jieba.load_userdict(infodir + "dictForJieba.txt")
            result = anls.textrank(ws[0])
            #print(result)
            return search_mult(result, a)
    else:
        return search_mult(ws, a)


class news:
    def __init__(self, title, time, page):
        self.title = title
        self.time = time
        self.page = page


class search_news:
    def __init__(self, title, time, abs, id, source):
        self.title = title
        self.time = time
        self.abs = abs
        self.id = id
        self.source = source


def initpage(request):
    return render(request, "init.html")


def detail(request, num):
    #print("detail")
    with open(dir + num + ".txt", 'r', encoding='utf-8') as f:
        title = f.readline()
        source = f.readline()
        time = f.readline()
        p = f.read()
        ps = dealRepeat.deal(p)
    context = {}
    context['title'] = title
    context['source'] = source
    context['time'] = time
    context['ps'] = ps
    return render(request, "detail.html", context)


def m_render(ind, ws):
    #print("m_render")
    res_list = []
    for i in ind:
        with open(dir + i + ".txt", 'r', encoding='utf-8') as g:
            title = g.readline()
            source = g.readline()
            time = g.readline()
            passage = g.read()
            now = 0
            start = -1
            while start == -1 and now < len(ws):
                start = passage.find(ws[now])
                now += 1
            abs = " - " + passage[max(start - 12, 0):min(start + 60, len(passage))] + "..."
            for word in ws:
                title = title.replace(word, "<em>" + word + "</em>")
                abs = abs.replace(word, r"<em>" + word + r"</em>")
            abs = abs.replace('\t', '')
            abs = abs.replace('\n', '')
            res_list.append(search_news(title, time, abs, i, source))
    return res_list


@csrf_exempt
def search(request):
    #print("search")
    start = time.time()
    word = request.POST['search_for']
    word = word.strip(' ')
    ws = word.split(' ')
    if '' in ws:
        ws.remove('')
    # print(ws)
    result = search_base(ws, 1)
    context = context_base(result[0], result[1], 1)
    end = time.time()
    context['title'] = word
    context['word'] = word
    context['first'] = True
    context['during_time'] = end - start
    return render(request, "search.html", context)


def search_pages(request, word, num):
    #print("search_pages")
    #print(word, num)
    a = int(num)
    ws = word.strip(' ').split(" ")
    result = search_base(ws, a)
    context = context_base(result[0], result[1], a)
    context['word'] = word
    context['first'] = False
    return render(request, "search.html", context)

from urllib import request
import re
from bs4 import BeautifulSoup
import time

def main():
    projectPath = "C:/Pytest/test1/"
    dir = projectPath + "NewsOrigin/"
    infodir = projectPath + "Info/"
    def sp(num = 0, stopurllist = []):
        startTime = None
        firstChildUrl = []
        maxNews = 3100
        maxRootNum = int((maxNews + 59) / 60)
        rooturlBase = "https://voice.hupu.com/nba/"
        started = False

        prevChildUrl = []
        for rootNum in range(0,maxRootNum):
            print(rootNum)
            rooturl = rooturlBase + str(rootNum + 1)
            reqroot = request.Request(rooturl)
            reqroot.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

            with request.urlopen(reqroot) as f:
                rootdata = f.read().decode('UTF-8',"ignore")
                # print (rootdata)
                soupRoot = BeautifulSoup(rootdata,features="html.parser")
                list = soupRoot.find_all('h4')
                childurl = []
                for item in list:
                    content = item.find_all('a')[0]["href"]
                    if (content not in prevChildUrl):
                        childurl.append(content)#防重复
                if rootNum == 0:
                    firstChildUrl = childurl
                prevChildUrl = childurl

                for i in childurl:
                    if (i in stopurllist):
                        return (num, startTime, firstChildUrl)

                    time.sleep(0.1)

                    # print(i)
                    req = request.Request(i)
                    req.add_header('User-Agent',
                                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

                    with request.urlopen(req) as g:
                        data = g.read().decode('UTF-8', "ignore")
                        soup = BeautifulSoup(data,features="html.parser")

                        title_div = soup.find('h1')
                        if (not bool(title_div)):
                            continue
                        title = title_div.get_text()
                        title = title.replace("\r\n","")
                        #title = title.replace("\n","")
                        title = title.strip(' ')
                        # print(title)

                        source_div = soup.find(id = "source_baidu")
                        source = source_div.find('a').get_text()
                        # print(source)

                        time_div = soup.find(id = "pubtime_baidu")
                        # print(time_div)
                        time_n = time_div.get_text()
                        time_n = time_n.strip(' ')
                        # print(time_n)

                        content_div = soup.find(class_ = "artical-main-content")
                        if (not bool(content_div)):
                            continue
                        content_p = content_div.find_all('p')
                        if (not bool(content_p)):
                            continue
                        if (startTime == None):
                            startTime = time_n
                        # print(content_p)
                        # print(dir + str(num) + ".txt")
                        file = open(dir + str(num) + ".txt", 'w', encoding="utf-8")
                        num += 1
                        file.write(title + '\n')
                        file.write(source + '\n')
                        file.write(time_n + '\n')
                        for i in content_p:
                            content = i.get_text()
                            file.write(content + '\n')
                        file.close()
        return (num, startTime, firstChildUrl)

    edNum = 0
    stNum = 0
    time_ = ""
    list = []
    try:
        with open(infodir + "sp.txt",'r',encoding="utf-8") as f:
            stNum = int(f.readline())
            edNum = int(f.readline())
            time_ = f.readline().strip('\n')
            list = f.readline().split(",")
            print(stNum, edNum)
            print([time_], list)
    except FileNotFoundError:
        print("err")

    (num_new, time_new, list_new) = sp(edNum, list)
    print(num_new)
    print(num_new-edNum)
    print([time_new])
    print(list_new)
    if (time_new == None):
        time_new = time_
    file = open(infodir + "sp.txt",'w',encoding="utf-8")
    file.write(str(stNum) + '\n')
    file.write(str(num_new) + '\n')
    file.write(time_new + '\n')
    file.write(",".join(list_new))
    return num_new-edNum

if __name__ == '__main__':
    print(main())
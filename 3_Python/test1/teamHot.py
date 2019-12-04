def main():
    projectPath = "C:/Pytest/test1/"
    infodir = projectPath + "Info/"
    dir = projectPath + "NewsOrigin/"
    newsdir = projectPath + "NewsHtml/"
    tardir = projectPath + "TeamNews/"
    fcpath = projectPath + "NewsFC/"

    #获取球队信息
    h = open(infodir + "dict.txt", 'r', encoding="utf-8")
    peopleDic = eval(h.read())
    h.close()
    h = open(infodir + "team.txt", 'r', encoding="utf-8")
    teamList = h.read().split(",")
    h.close()
    print(peopleDic)
    print(teamList)

    #获取添加html的下标
    stNum = 0
    teamHot = dict([(x,0) for x in teamList])
    try:
        with open(infodir + "hot.txt",'r',encoding="utf-8") as f:
            stNum = int(f.readline())+1
            teamHot = eval(f.read())
    except FileNotFoundError:
        print("err: No File")
    f = open(infodir + "sp.txt",'r',encoding="utf-8")
    edNum = int(f.read().split('\n')[1])+1
    f.close()
    print(stNum,edNum)
    print(list(range(stNum, edNum)))
    #开始添加并计数
    for stNum in range(stNum, edNum):
        if (stNum % 100 == 0):
            print(stNum)
        teamContain = set()
        with open(dir + str(stNum) + ".txt", 'r', encoding="utf-8") as file:
            data = file.read()
        for team in teamList:
            if data.find(team) >= 0:
                teamContain.add(team)
        for person in peopleDic:
            if data.find(person) >= 0:
                for x in peopleDic[person]:
                    teamContain.add(x[0])
        #print(teamContain)
        for team in teamContain:
            teamHot[team] = teamHot[team] + 1
            with open(tardir + team + ".txt", 'a', encoding="utf-8") as wfile:
                wfile.write(str(stNum))
                wfile.write(' ')
    print(teamHot)
    hot_str = "{" + ','.join(["\'%s\':%s" % (key, value) for key, value in teamHot.items()]) + "}"
    stNum = min(stNum,edNum-1)
    with open(infodir + "hot.txt", 'w', encoding="utf-8") as f:
        f.write(str(stNum) + '\n')
        f.write(hot_str)
    # for team in teamList:
    #     with open(tardir + team + ".txt", 'r', encoding="utf-8") as wfile:
    #         print(wfile.read())

if __name__ == '__main__':
    print(main())
def deal(str):
    print(str)
    print(str.split('\n'))
    projectPath = "C:/Pytest/test1/"
    infodir = projectPath + "Info/"
    with open(infodir + "repeat.txt",'r',encoding="utf-8") as f:
        repeat = eval(f.read())
    with open(infodir + "dict.txt", 'r', encoding="utf-8") as f:
        d = eval(f.read())
    with open(infodir + "team.txt", 'r', encoding="utf-8") as f:
        tt = f.read().split(',')

    highlight = set()
    for person in d:
        if str.find(person) >= 0:
            highlight.add(person)
    print(len(highlight),highlight)

    for person in highlight.copy():
        if person in repeat:
            for sub in repeat[person]:
                if sub in highlight:
                    highlight.remove(sub)
    print(len(highlight),highlight)
    for team in tt:
        str = str.replace(team, "<a href=\"/team/" + team + "\">" + team + "</a>")
    print(str)
    print(str.split('\n'))
    for person in highlight:
        str = str.replace(person, "<a href=\"/team/" + d[person][0][0] + "\">" + person + "</a>")
        print(str)
    return str.split('\n')


if __name__ == '__main__':
    deal("汤普汤普森啦啦啦")
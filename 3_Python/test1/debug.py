from test1 import sp, fc, teamHot


projectPath = "C:/Pytest/test1/"
infodir = projectPath + "Info/"


def run():
    try:
        with open(infodir + "spState.txt", 'r', encoding='utf-8') as f:
            if f.readline() == "running\n":
                print(0)
                return 0
    except:
        pass
    with open(infodir + "spState.txt", 'w', encoding='utf-8') as f:
        f.write("running\n")
    print(sp.main())
    with open(infodir + "spState.txt", 'r', encoding='utf-8') as f:
        if f.read() != "running\n":
            print(1)
            return 1
    print(fc.main())
    with open(infodir + "spState.txt", 'r', encoding='utf-8') as f:
        if f.read() != "running\n":
            print(2)
            return 2
    print(teamHot.main())
    with open(infodir + "spState.txt", 'r', encoding='utf-8') as f:
        if f.read() != "running\n":
            print(3)
            return 3
    with open(infodir + "spState.txt", 'w', encoding='utf-8') as f:
        f.write("stopped\n")
        print(4)
        return 4

run()
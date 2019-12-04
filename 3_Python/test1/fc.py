import jieba
def main():
    projectPath = "C:/Pytest/test1/"
    path = projectPath + "NewsOrigin/"
    infodir = projectPath + "Info/"
    tarpath = projectPath + "NewsFC/"
    file = open(infodir + "sp.txt",'r',encoding="utf-8")
    dt = file.read().split('\n')
    start = int(dt[0])
    end = int(dt[1])
    file.close()
    print(start,end)
    for i in range(start, end):
        print(i)
        a = []
        with open(path + str(i) + ".txt", 'r', encoding="utf-8") as file:
            data = file.read()
            #print(data)
            seg_list = jieba.cut_for_search(data)
            for tk in seg_list:
                if(not (tk in a)):
                    a.append(tk)
            for j in a:
                if (j == '\n' or j == '\t' or j == '?' or j == ' ' or j == ':' or j == "\"" or j == "<" or j == ">" or j == "/" or j == "\\" or j == "*" or j == "|"):
                    continue
                with open(tarpath + j + ".txt", 'a', encoding="utf-8") as wfile:
                    wfile.write(str(i))
                    wfile.write(' ')
    file = open(infodir + "sp.txt",'w',encoding="utf-8")
    dt[0] = str(end)
    file.write('\n'.join(dt))
    file.close()
    return end


if (__name__ == '__main__'):
    print(main())
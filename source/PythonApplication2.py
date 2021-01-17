
class KB:
    def __init__(self, sentence):
        self.clauses = []
        if sentence:
            self.tell(sentence)
    def tell(self, sentence):
        self.clauses.extend(sentence)

def negative(alpha):
    if '-' in alpha:
        alpha = alpha.replace('-','')
    else:
        alpha = '-' + alpha
    return alpha

def sort(a):
    tempA = a
    tempA = tempA.replace('-','')
    tempA = tempA.split()
    tempA.sort()
    clauses = []
    for i in tempA:
        for j in range(len(a)):
            if a[j] == i and a[j-1] == '-':
                clauses.append('-')
        clauses.append(i)
    result = clauses[0]
    if len(clauses) > 0:
        for x in range(len(clauses) -1):
            if clauses[x] != '-':
                result = result + " " + clauses[x+1];
            else:
                result = result + clauses[x+1];
    return result

def coKhaNangHopGiai(ci, cj):
    #Kiểm tra đối
    cauI = ci.split(" ")
    check = 0
    for i in cauI:
        i = negative(i)
        if i in cj:
            check = 1
    cauJ = cj.split(" ")
    for j in cauJ:
        j = negative(j)
        if j in ci:
            check = 1
    if check == 1:
        return check
    #Kiểm tra trùng
    #ci
    count = 0
    for i in cauI:
        if i in cauJ:
            count = count + 1
    if count != 0:
        return 0
    #cj
    count = 0
    for j in cauJ:
        if j in cauI:
            count = count + 1
    if count != 0:
        return 0
    return 0

def hopGiai_KhongCanThiet(ci,cj):
    ci_clause = ci.split()
    cj_clause = cj.split()
    ci_count = len(ci_clause)
    cj_count = len(cj_clause)
    #ci
    count = 0
    for i in ci_clause:
        if i in cj_clause:
            count = count + 1
    if count == ci_count:
        return 1
    #cj
    count = 0
    for j in cj_clause:
        if j in ci_clause:
            count = count + 1
    if count == cj_count:
        return 1
    return 0

def PL_RESOLUTION(KB, alpha):
    fileOutput = open("output.txt","w")
    clauses = []
    clausesx = KB.clauses
    clauses.append(negative(alpha))

    clauses = clauses + clausesx
    new = []
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j])for i in range(n) for j in range(i+1, n)]
        for (ci, cj) in pairs:
            ##Loại các câu không thể hợp giải
            check = coKhaNangHopGiai(ci,cj)
            if check == 0:
                continue
            ##Loại các câu hợp giải không cần thiết
            check = hopGiai_KhongCanThiet(ci,cj)
            if check == 1:
                continue

            resolvents = pl_resolve(ci, cj)            
            myNew = []
            resolventsCount = 0
            for temp in resolvents:
                if temp == "{}" or temp == "{":
                    resolventsCount += 1
                    fileOutput.write(str(resolventsCount))
                    fileOutput.write("\n")
                    for index in range(resolventsCount-1):
                        fileOutput.write(myNew[index])
                        fileOutput.write("\n")
                    fileOutput.write("{}\nYES")
                    fileOutput.close()
                    return True
            for index in range(len(resolvents)):
                resolvents[index] = sort(resolvents[index])
                if resolvents[index] not in clauses:
                    resolventsCount += 1;
                    myNew.append(resolvents[index])
                new.append(resolvents[index])
        # if new ⊆ clauses then return false
        count = 0
        newLen = len(new)
        for c in new:
            if c in clauses:
                count = count + 1
        ##print(count , newLen)
        if count == newLen:
            fileOutput.write("0\nNO")
            fileOutput.close()
            return False
        # clauses ← clauses ∪ new
        textResult = []
        textResultCount = 0
        for c in new:
            if c not in clauses: 
                clauses.append(c)
                textResult.append(c)
                textResultCount += 1

        #ghi vao file
        fileOutput.write(str(textResultCount))
        fileOutput.write("\n")
        for index in range(textResultCount):
            fileOutput.write(textResult[index])
            fileOutput.write("\n")
        ##print(textResultCount,textResult)

def pl_resolve(ci, cj):
    if '--' in ci:
        ci = ci.replace('--','')
    if '--' in cj:
        cj = cj.replace('--','')
    ## remove or
    ci_clause = ci.split()
    cj_clause = cj.split()
    for i in ci_clause:
        if i == "or" or i == "OR":
            ci_clause.remove(i)
    for j in cj_clause:
        if j == "or" or j == "OR":
            cj_clause.remove(j)
    result = []
    ## remove same A A
    for i in ci_clause:
        for j in cj_clause:
            if i == j:
                cj_clause.remove(j)
    ## remove opposite A -A
    for i in ci_clause:
        for j in cj_clause:
            if i == '-'+j or '-'+i == j:        
                clauses = ci_clause + cj_clause
                clauses.remove(i)
                clauses.remove(j)
                if clauses == []:
                    return "{}"
                bienChay = 0
                for ii in clauses:
                    for jj in clauses:
                        if ii == negative(jj):
                            bienChay += 1
                            break
                if bienChay == 0:
                    result1 = clauses[0]
                    if len(clauses) > 0:
                        for x in range(len(clauses) -1):
                            result1 = result1 + " " + clauses[x+1];
                    result.append(result1)
                else:
                    continue
    return result

def main():
    fo = open("input.txt", "r")
    if not fo.readable():
        print("Loi khong tim thay file")
        return
    data = fo.read()
    line = data.splitlines()
    ##print(line)
    alpha = line[0]
    print("alpha ", alpha)
    num = line[1]
    num = (int)(num)
    clauses = []
    for i in range(num):
        Tempclause = line[i +2]
        Tempclause = Tempclause.replace(" OR","")
        Tempclause = sort(Tempclause)
        clauses.append(Tempclause)
        print(Tempclause)
    ##print(clauses)
    kb = KB(clauses)
    print("------------------")
    ex = PL_RESOLUTION(kb, alpha)
    print(ex)
main()
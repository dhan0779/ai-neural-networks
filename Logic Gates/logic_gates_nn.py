import sys,math,time,random
def main():
    x = time.time()
    real = []
    inpfile = open(sys.argv[1],"r")
    for line in inpfile:
        fakelist = []
        line = line.split(" ")
        for ch in line:
            if ch != "=>":
                fakelist.append(int(ch))
        real.append(fakelist)
    input = []
    for lis in real:
        hi = []
        for ch in lis:
            hi.append(ch)
        hi.pop()
        hi.append(1)
        input.append(hi)

    weights = [[random.uniform(-2,2)]*(2*len(input[0])),[random.uniform(-2,2),random.uniform(-2,2)],[random.uniform(-2,2)]]
    alpha = 0.3
    totalerror = 1
    iterations = 0
    it10 = 0
    while totalerror > 0.0009:
        totalerror = 0
        for i in range(0,len(input)):
            ff = forwardfeed(input[i],weights,"T3")
            errort = error(ff[len(ff)-1][0],real[i][len(real[i])-1])
            totalerror += errort
            weights = backpropagation(ff,weights,"T3",real[i][len(real[i])-1],alpha)
        iterations+=1
        if iterations != 0 and iterations%10 == 0 and totalerror > 0.1:
            if abs(totalerror-it10) < 0.0001:
                weights = [[random.uniform(-2, 2)] * (2 * len(input[0])),[random.uniform(-2, 2), random.uniform(-2, 2)], [random.uniform(-2, 2)]]
                iterations = 0
            else: it10 = totalerror+1-1


    print("Layer cts:", [len(input[0]), 2, 1, 1])
    print("Weights:")
    print(weights[0])
    print(weights[1])
    print(weights[2])
    print(totalerror)

def error(ffval,actual):
    return 0.5*((actual-ffval)**2)

def transfer(input,x):
    if input == "T1": return x
    if input =="T2":
        if x < 0: return 0
        else: return x
    if input == "T3": return 1/(1+math.e**-x)
    if input == "T4": return (2 / (1 + math.exp(-1 * x))) - 1

def transfersderiv(input,x):
    if input == "T1": return 1
    if input =="T2":
        if x < 0: return 0
        else: return 1
    if input == "T3": return x*(1-x)
    if input == "T4": return (1-x**2)/2

def dot(list1,list2):
    return sum(i[0] * i[1] for i in zip(list1, list2))

def forwardfeed(inputs,weights,transfers):
    layerC = [inputs]
    tmp = []
    fin = []
    for i in range(len(weights)):
        current = weights[i]
        next = []
        if i != len(weights) - 1:
            for j in range(len(current)):
                tmp.append(weights[i][j])
                if len(inputs) != 1 and j != 0 and (j+1) % (len(inputs)) == 0:
                    next.append(dot(tmp,inputs))
                    tmp = []
                if len(inputs) == 1:
                    next.append(dot(tmp, inputs))
                    tmp = []
            fin = []
            for elem in next:
                fin.append(transfer(transfers,elem))
                next = fin
        else:
            fin = []
            for z in range(len(inputs)):
                fin.append(inputs[z]*current[z])
        inputs = fin
        layerC.append(inputs)
    return layerC

def backpropagation(inputs,weight,transfersder,real,alpha):
    newWeights = [[],[],[]]
    E_list = [[],[],[],[]]
    for i in range(len(inputs)-1,0,-1):
        if i == len(inputs)-2:
            E_list[i].append((E_list[i+1][0])*weight[i][0]*transfersderiv(transfersder,inputs[i][0]))
            newWeights[i-1].append(E_list[i][0]*inputs[i-1][0]*alpha+weight[i-1][0])
            newWeights[i-1].append(E_list[i][0]*inputs[i-1][1]*alpha+weight[i-1][1])
        elif i == len(inputs)-1:
            E_list[i].append(real-inputs[i][0])
            newWeights[i-1].append(E_list[i][0]*inputs[i-1][0]*alpha+weight[i-1][0])
        else:
            for z in range(0,len(inputs[i])):
                sum = 0
                weightsum = z
                for g in range(len(inputs[i+1])): #fix here
                    sum += weight[i][weightsum]*E_list[i+1][g]
                    weightsum+=len(inputs[i])
                E_list[i].append((sum)*transfersderiv(transfersder,inputs[i][z]))
            countw = 0
            for u in range(len(inputs[i])):
                for j in range(len(inputs[i-1])):
                    newWeights[i-1].append(E_list[i][u]*inputs[i-1][j]*alpha+weight[i-1][countw])
                    countw+=1
    return newWeights

if __name__ == '__main__':
    main()
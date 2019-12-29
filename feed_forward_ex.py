import math,sys
def transfer(input,x):
    if input == "T1":
        return x
    if input =="T2":
        if x < 0:
            return 0
        else:
            return x
    if input == "T3":
        return 1 / (1 + math.exp(-1 * x))
    if input == "T4":
        return (2 / (1 + math.exp(-1 * x))) - 1

def dot(list1,list2):
    return sum(i[0] * i[1] for i in zip(list1, list2))

def main():
    weight = sys.argv[1]
    transfers = sys.argv[2]
    inputs = [float(x) for x in sys.argv[3:]]
    weight1 = open(weight).read().splitlines()
    weights = [[float(z) for z in y.split(" ")] for y in weight1]
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
    print(inputs)


if __name__ == '__main__':
    main()
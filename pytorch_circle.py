import sys
import torch
import torch.nn as nn
import random
import time
hi= time.time()
equation = sys.argv[1]
symbol = False
equation = equation.replace("=","")
ind = equation.find("<")
if ind == -1:
    ind = equation.find(">")
    symbol = True

insert = []
expect = []
for i in range(10000):
    x = random.uniform(-1.5,1.5)
    y = random.uniform(-1.5,1.5)
    insert.append([x,y])
    if symbol == False and (x**2 + y**2) < float(equation[ind+1:]): expect.append([1.0])
    elif symbol == True and (x**2 + y**2) > float(equation[ind+1:]): expect.append([1.0])
    else: expect.append([0.0])
ins = torch.tensor(insert)
expected = torch.tensor(expect)
nodeCts = [len(ins[0]), 2, 1]

mynn = torch.nn.Sequential(torch.nn.Linear(len(ins[0]),20),torch.nn.Sigmoid(),torch.nn.Linear(20,5),torch.nn.Sigmoid(), torch.nn.Linear(5,1),torch.nn.Sigmoid(),torch.nn.Linear(1,1,bias=False))
criterion = torch.nn.MSELoss()

optimizer = torch.optim.SGD(mynn.parameters(), lr=2)
for epoch in range(40000+1):
    y_pred = mynn(ins) # Forward propagation
    loss = criterion(y_pred, expected) # Compute and print error
    if not epoch%500 or epoch<10:
        print('epoch: ', epoch,' loss: ', loss.item())
    optimizer.zero_grad() # Zero the gradients
    loss.backward() # Back propagation
    optimizer.step() # Update the weights
    if time.time()-hi > 90 or loss.item() < 0.003:
        print(time.time()-x)
        counter = 0
        print("Layer cts:", [2,20,5,1,1])
        print("Weights:")
        for k,v in mynn.state_dict().items():
            if counter%2==0: print(v.flatten().tolist())
            counter+=1
        break

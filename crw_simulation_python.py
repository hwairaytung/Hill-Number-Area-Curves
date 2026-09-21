import math
from datetime import datetime
import json
import random

L=100
max_r = 1.3

N = int(L**max_r)
alpha = 1/L**2

#Store site (x,y) as integer
def pair(x, y):
    if x>=0:
        x = 2*x
    else:
        x = -2*x-1
    if y>=0:
        y = 2*y
    else:
        y = -2*y-1
    return (x+y)*(x+y+1)//2 + y

#Undoes the pair function and turns integer into site (x, y)
def unpair(z):
    w = math.floor((math.sqrt(8 * z + 1) - 1) / 2)
    t = (w**2 + w) // 2
    y = z - t
    x = w - y
    if x%2 == 0:
        x = x//2
    else:
        x = -(x+1)//2
    if y%2 == 0:
        y = y//2
    else:
        y = -(y+1)//2
    return x, y

#Get a neighboring space
def next_spot(current_spot):
    x, y = unpair(current_spot)
    yay = random.random()
    if yay<0.25:
        return pair(x+1, y)
    elif yay<0.5:
        return pair(x-1, y)
    elif yay<0.75:
        return pair(x, y+1)
    else:
        return pair(x, y-1)

#initiallize a dictionary of the coalescing walkers where 
#the key is the location of the walker and the value is a list of
#integers representing the sites at present that are descendants
#of the walker.
current_walkers = dict()
for i in range(N):
    for j in range(N):
        current_walkers[pair(i, j)] = [i*N+j]

#The main process
result = []
while len(current_walkers)>1:
	#pick a walker
    walker = random.choice(list(current_walkers))
    #if walker mutates, remove from CRW system and add descendant sites to the result list
    if random.random() < alpha/(1+alpha):
        result.append(current_walkers.pop(walker))
        print(len(current_walkers))
    #if walker moves, check if it coalesced with another walker
    else:
        new_dest = next_spot(walker)
        if new_dest in current_walkers:
            current_walkers[new_dest].extend(current_walkers.pop(walker))
        else:
            current_walkers[new_dest] = current_walkers.pop(walker)

if len(current_walkers) == 1:
    result.append(current_walkers[list(current_walkers)[0]])

#Print time the code finishes and output result in json format.
now = datetime.now()
formatted_date = now.strftime("%Y%m%d%H%M%S")
with open("CRW_L"+str(L)+'_'+formatted_date+".json", 'w') as f:
    json.dump(result, f)


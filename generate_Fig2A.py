import json
import glob
import numpy as np
import pickle

import matplotlib.pyplot as plt
import seaborn as sns

L=100

rs = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
max_rs = 2

#Get the file with the data output
files = glob.glob('CRW_L'+str(L)+'_*.json')
file = files[0]

#Get length of side of box the data does
Nmax=int(L**max_rs)

#Open file and get the clusters of species
with open(file, 'r') as f:
    clusters = json.load(f)

#Construct a 2D matrix. Populate so that sites with the same integer 
#belongs to the same species, and vice versa
all_states = np.zeros((Nmax, Nmax), dtype = np.int32)
for i in range(len(clusters)):
    all_states[tuple(np.array([[j%Nmax, j//Nmax] for j in clusters[i]]).T)] = i

#Record the 0, 1, and 2 Hill numbers. 
#For r>1.5, we work with the clusters data directly rather than the all_states
#matrix for memory reasons.
q0d, q1d, q2d = [], [], []
for r in rs:
    N=int(L**r)
    if r == 2.0:
        species_sizes = np.array([len(cluster) for cluster in clusters])
        q0d.append(len(species_sizes))
        q1d.append(np.exp(-np.sum(species_sizes/N**2*(np.log(species_sizes) - 2*np.log(N)))))
        q2d.append(1/np.sum(species_sizes*species_sizes/N**4))
    elif r > 1.5:
        species_sizes = np.array([np.sum((np.array(cluster)%Nmax<N)*(np.array(cluster)//Nmax<N)) for cluster in clusters])
        species_sizes = species_sizes[species_sizes > 0]
        q0d.append(len(species_sizes))
        q1d.append(np.exp(-np.sum(species_sizes/N**2*(np.log(species_sizes) - 2*np.log(N)))))
        q2d.append(1/np.sum(species_sizes*species_sizes/N**4))
    else:
        view = all_states[0:N, 0:N]#all_states[Nmax-N:Nmax, Nmax-N:Nmax]
        species = np.unique(view)
        species_sizes = np.array([np.sum(view==specie) for specie in species])
        q0d.append(len(species))
        q1d.append(np.exp(-np.sum(species_sizes/N**2*(np.log(species_sizes) - 2*np.log(N)))))
        q2d.append(1/np.sum(species_sizes*species_sizes/N**4))
    print(r)

#Compute the actual r exponent since our box lengths are integers
actual_rs = [np.log(int(L**r))/np.log(L) for r in rs]

#plot results
plt.scatter(actual_rs, np.log(q0d)/(2*np.log(L)), label="q=0")    
plt.scatter(actual_rs, np.log(q1d)/(2*np.log(L)), label="q=1")  
plt.scatter(actual_rs, np.log(q2d)/(2*np.log(L)), label="q=2") 
plt.ylabel('ln(${}^q$D)/(2ln(L))')
plt.xlabel('r')
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim([0.97, 2.03])
plt.ylim([0, 1.4])
plt.legend(loc=2) 
plt.savefig('beyondR1.png', dpi=200)
plt.show()
plt.close()
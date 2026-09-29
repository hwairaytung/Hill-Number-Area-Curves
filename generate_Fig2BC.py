import json
import glob
import numpy as np

import matplotlib.pyplot as plt

L=400 #Set to 400 for 2B and 1600 for 2C

if L==400:
    rs = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0, 1.1, 1.2, 1.3]
elif L==1600:
    rs = np.arange(41)/40

files = glob.glob('CRW_L'+str(L)+'_*.json')

Nmax=int(L**max(rs))

def get_all_states(Nmax, file):
    with open(file, 'r') as f:
        clusters = json.load(f)
    all_states = np.zeros((Nmax, Nmax), dtype = np.int32)
    for i in range(len(clusters)):
        all_states[tuple(np.array([[j%Nmax, j//Nmax] for j in clusters[i]]).T)] = i
    return all_states

all_q0d, all_q1d, all_q2d = [], [], []
actual_rs = [np.log(int(L**r))/np.log(L) for r in rs]
for file in files:
    all_states = get_all_states(Nmax, file)
    
    q0d, q1d, q2d = [], [], []
    for r in rs:
        N=int(L**r)
        view = all_states[0:N, 0:N]
        species = np.unique(view)
        species_sizes = np.array([np.sum(view==specie) for specie in species])
        q0d.append(len(species))
        q1d.append(np.exp(-np.sum(species_sizes/N**2*(np.log(species_sizes) - 2*np.log(N)))))
        q2d.append(1/np.sum(species_sizes*species_sizes/N**4))
    
    all_q0d.append(q0d)
    all_q1d.append(q1d)
    all_q2d.append(q2d)
    
if L == 400:
    plt.scatter(actual_rs, np.mean(np.log(all_q0d)/(2*np.log(L)), axis = 0), label="q=0")    
    plt.scatter(actual_rs, np.mean(np.log(all_q1d)/(2*np.log(L)), axis = 0), label="q=1")  
    plt.scatter(actual_rs, np.mean(np.log(all_q2d)/(2*np.log(L)), axis = 0), label="q=2") 
    plt.ylabel('ln(${}^q$D)/(2ln(L))')
    plt.xlabel('r')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim([0, 1.35])
    plt.ylim([0, 0.7])
    plt.legend(loc=4)
    plt.savefig(str(L)+'.png', dpi=200)
    plt.show()
    plt.close()   

if L == 1600:
    plt.plot(actual_rs, np.mean(np.log(all_q2d)/(2*np.log(L)), axis = 0), lw = 5, color = 'black')
    plt.plot(actual_rs, np.log(all_q2d[0])/(2*np.log(L)), color = 'gray', ls = '-.')
    plt.plot(actual_rs, np.log(all_q2d[2])/(2*np.log(L)), color = 'darkgray', ls='--')
    plt.plot(actual_rs, np.log(all_q2d[8])/(2*np.log(L)), color = 'lightgray', ls='-')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim([0, 1])
    plt.ylim([0, 0.2])
    plt.ylabel('ln(${}^2$D)/(2ln(L))')
    plt.xlabel('r')
    plt.savefig(str(L)+'.png', dpi=200)
    plt.show()
    plt.close()

import os
import pdb
import random
import copy

import numpy as N
import matplotlib as M
import matplotlib.pyplot as plt
from tqdm import tqdm

class FHP:
    def __init__(self,ncols=500,nrows=500,IC_random=True):
        self.ncols = ncols
        self.nrows = nrows
        self.lattice = self.create_lattice()
        self.coords = self.get_coords()
        self.fill_random()
        # pdb.set_trace()

    def create_lattice(self):
        init_lattice = N.zeros((self.nrows,self.ncols),dtype=N.object)
        for i in range(self.nrows):
            for j in range(self.ncols):
                init_lattice[i,j] = self.create_node()
        return init_lattice

    def create_node(self,):
        class node:
            def __init__(self,):
                self.ni_s = N.zeros([6])
                self.occupied = False
                return

        return node()

    def get_occupied_array(self):
        arr = N.zeros_like(self.lattice,dtype=N.bool)
        it = N.nditer(arr,flags=['multi_index'])
        for boo in it:
            x,y = it.multi_index
            arr[x,y] = self.lattice[x,y].occupied
        return arr

    def viz_one_time(self,nn,save=True,fpath=None):
        if not fpath:
            fpath = f'figs/test_{nn}.png'
        fig,ax = plt.subplots(1,figsize=(6,6),dpi=300)
        data = self.get_occupied_array()
        ax.imshow(data,vmin=0,vmax=1,cmap=M.cm.binary)
        fig.savefig(fpath)
        plt.close(fig)
        # pdb.set_trace()
        return

    def get_neighbours(self,coords):
        row,col = coords
        neighs = []

        neighs.append([row,(col+1)%self.ncols]) # RIGHT
        neighs.append([(row-1)%self.nrows,(col+1)%self.ncols]) # TOP RIGHT
        neighs.append([(row-1)%self.nrows,(col-1)%self.ncols]) # TOP LEFT
        neighs.append([row,(col-1)%self.ncols]) # LEFT 
        neighs.append([(row+1)%self.nrows,(col-1)%self.ncols]) # BOTTOM LEFT
        neighs.append([(row+1)%self.nrows,(col+1)%self.ncols])
        return neighs

    def get_coords(self,):
        ii, jj = N.meshgrid(N.arange(self.nrows),N.arange(self.ncols),
                    indexing='ij')
        coord_grid = N.array([ii,jj])

        all_coords = []
        for i in range(1,self.nrows-1):
            for j in range(1,self.ncols-1):
                all_coords.append(list(coord_grid[:,i,j]))

        return all_coords

    def fill_random(self,nsamples=10000,d=False):
        # Should "d" be an integer or bool?!
        samples = random.sample(self.coords,nsamples)

        for r,c in samples:
            self.lattice[r,c].occupied = True
            these_neighs = self.get_neighbours([r,c])

            while True:
                if not d:
                    direction = random.choice([i for i in range(6)])
                else:
                    direction = d-1
                nr,nc = these_neighs[direction]
                if not self.lattice[nr,nc].occupied:
                    self.lattice[nr,nc].ni_s[direction] = 1
                    break
        # pdb.set_trace()
        return

    def headon(self,n,i):
        return n[i%6] * n[(i+3)%6] * (1-n[(i+1)%6]) * (
                1-n[(i+2)%6]) * (1-n[(i+4)%6])

    def threebody(self,n,i):
        return n[i] * n[(i+2)%6] * n[(i+4)%6] * (
                1-n[(i+1)%6]) * (1-n[(i+3)%6]) * (1-n[(i+5)%6])

    def collision_factor(self,coords,i):
        q = random.choice([0,1])
        r,c = coords
        n = self.lattice[r,c].ni_s
        omega = -self.headon(n,i) + q*self.headon(n,(i-1)%6) + (
                    (1-q)*self.headon(n,(i+1)%6) - self.threebody(
                    n,i)+self.threebody(n,(i+3)%6))
        return omega

    def update(self,):
        # Create function for creating a new grid?
        lattice_new = self.create_lattice()
        for r in N.arange(self.nrows):
            for c in N.arange(self.ncols):
                these_neighs = self.get_neighbours([r,c])
                for i in range(6):
                    if self.lattice[r,c].ni_s[i] > 0:
                       lattice_new[r,c].occupied = True
                       sent_r, sent_c = these_neighs[(i+3)%6]
                       lattice_new[r,c].ni_s[i] = 0

                    that_r, that_c = these_neighs[i]
                    lattice_new[that_r,that_c].ni_s[i] = lattice_new[
                        r,c].ni_s[i]+self.collision_factor([r,c],i)
        self.lattice[:,:] = lattice_new[:,:]
        return

    def update_LBCs(self):
        lattice_new = self.create_lattice()
        for r in N.arange(self.nrows):
            for c in N.arange(self.ncols):
                these_neighs = self.get_neighbours([r,c])
                for i in range(6):
                    that_r, that_c = these_neighs[i]
                    lattice_new[that_r,that_c].ni_s[i] = self.lattice[
                        r,c].ni_s[i]+collision_factor([r,c],self.lattice,i)

                    if self.lattice[r,c].ni_s > 0:
                        lattice_new[r,c].occupied = True
                        a_r,a_c = these_neighs[i]
                        lattice_new[a_r,a_c].occupied = False
                        lattice_new[r,c].ni_s = 0

    def viz_states(self,):
        lattice_copy = N.copy(self.lattice)
        for i in range(lattice_copy.shape[0]):
            for j in range(lattice_copy.shape[1]):
                lattice_copy[i,j] = self.lattice[i,j].occupied

            


if __name__ == '__main__':
    fhp = FHP(nrows=500,ncols=500,IC_random=True)
    # fhp.viz_one_time(1)
    states = [fhp.get_occupied_array(),]
    for i in range(20):
        fhp.update()
        states.append(fhp.get_occupied_array())
    # fhp.viz_one_time(2)
    # pdb.set_trace()


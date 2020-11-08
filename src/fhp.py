import os
import pdb

import numpy as N 

class FHP:
    """Lattice gas PCA
    """
    
    def __init__(self,):
        numnodes_x = 3200/10
        nummodes_y = 3200/10
        
        # Total timesteps to simulate
        t_end = 5
        
        nodes = N.zeros([nummodes_x,nummodes_y,6])
            
        # Defime the possible velocities (i.e. unit directions in 2D)
        C = N.array([5,2])
        for i in N.range(5):
            C[i,:] = [N.cos((i*N.pi)/3); N.sin((i*N.pi)/3)]

        
    def simulate(self,):
        numparts = N.sum(nodes)
        for t in N.arange(t_end):
            for i in N.arange(1,numnodes_x-1):
                for j in N.arange(1,numnodes_y-1):
                    # A bad way of doing things     
                    
                    # Modify nodes with new values
                    # Mask for cell sum = 1 or 2
                    # cm1 = 0
                    # These cells do not change
                    # pass 
                    
                    # If cell sum = 2
                    # Mask cm2 = 0
                    
                    # In that slice, find 3-particle
                    # where nodes[cm2] [1==3] and [3==5]
                    # where cm2[1,3,5]?
                    # Invert 
                    # nodes[where] = ~nodes[where]
                    # else:
                    # don't change - pass 
                    
                    # 2-particle collision
                    loc = N.where(nodes,0)
                    
                    # If opposite cell is occupied
                    if (loc>2) or (nodes[loc+2) != 1):
                        pass
                    else:
                         # Randomly rotate clockwise or anti-clockwise
                        r = N.random(0,1)
                        if r<0.5:
                         n_cell
                    
            


#****************************************************#
# This file is part of OPTALG.                       #
#                                                    #
# Copyright (c) 2015-2016, Tomas Tinoco De Rubira.   #
#                                                    #
# OPTALG is released under the BSD 2-clause license. #
#****************************************************#

from __future__ import print_function
import time
import numpy as np
from numpy.linalg import norm
from scipy.sparse import coo_matrix
from .stoch_solver import StochSolver

class StochHybridPD(StochSolver):
    
    parameters = {'maxiters': 1000,
                  'maxtime': 600,
                  'period': 60,
                  'quiet' : True,
                  'theta': 1.,
                  'k0': 0,
                  'no_G': False,
                  'warm_start': False}

    name = 'Primal-Dual Stochastic Hybrid Approximation'

    def __init__(self):
        """
        Primal-Dual Stochastic Hybrid Approximation Algorithm.
        """
        
        # Init
        StochSolver.__init__(self)
        self.parameters = StochHybridPD.parameters.copy()
        
        self.results = []

    def solve(self,problem):
        
        # Local vars
        params = self.parameters
        
        # Parameters
        maxiters = params['maxiters']
        maxtime = params['maxtime']
        period = params['period']
        quiet = params['quiet']
        theta = params['theta']
        warm_start = params['warm_start']
        k0 = params['k0']
        no_G = params['no_G']
        
        # Header
        if not quiet:
            print('\nPrimal-Dual Stochastic Hybrid')
            print('-----------------------------')
            print('{0:^8s}'.format('iter'), end=' ')
            print('{0:^10s}'.format('time(s)'), end=' ')
            print('{0:^10s}'.format('alpha'), end=' ')
            print('{0:^12s}'.format('prop'), end=' ')
            print('{0:^12s}'.format('lmax'), end=' ')
            print('{0:^12s}'.format('EF_run'), end=' ')
            print('{0:^12s}'.format('EGmax_run'), end= ' ')
            print('{0:^12s}'.format('saved'))

        # Init
        k = 0
        t1 = 0
        sol_data = None
        t0 = time.time()
        g = np.zeros(problem.get_size_x())
        lam = np.zeros(problem.get_size_lam())
        J = coo_matrix((problem.get_size_lam(),problem.get_size_x()))
        self.results = []

        # Loop
        while True:

            # Steplength
            alpha = theta/(k0+k+1.)

            # Solve approx
            if warm_start:
                self.x,gF_approx,JG_approx,sol_data = problem.solve_Lrelaxed_approx(lam,g_corr=g,J_corr=J,quiet=True,init_data=sol_data)
            else:
                self.x,gF_approx,JG_approx,sol_data = problem.solve_Lrelaxed_approx(lam,g_corr=g,J_corr=J,quiet=True)
                
            # Sample
            w = problem.sample_w()
            
            # Eval
            F,gF,G,JG = problem.eval_FG(self.x,w)
            
            # Running
            if k == 0:
                EF_run = F
                EG_run = G.copy()
            else:
                EF_run += alpha*(F-EF_run)
                EG_run += alpha*(G-EG_run)
 
            # Save
            if time.time()-t0 > t1:
                self.results.append((k,time.time()-t0,self.x,np.max(lam)))
                t1 += period

            # Iters
            if k >= maxiters:
                break
                
            # Maxtime
            if time.time()-t0 >= maxtime:
                break

            # Output
            if not quiet:
                print('{0:^8d}'.format(k), end=' ')
                print('{0:^10.2f}'.format(time.time()-t0), end=' ')
                print('{0:^10.2e}'.format(alpha), end=' ')
                print('{0:^12.5e}'.format(problem.get_prop_x(self.x)), end=' ')
                print('{0:^12.5e}'.format(np.max(lam)), end=' ')
                print('{0:^12.5e}'.format(EF_run), end=' ')
                print('{0:^12.5e}'.format(np.max(EG_run)), end=' ')
                print('{0:^12d}'.format(len(self.results)))
                               
            # Update
            if not no_G:
                lam = problem.project_lam(lam + alpha*G)
            g += alpha*(gF-gF_approx-g)
            J = J + alpha*(JG-JG_approx-J)
            k += 1
            
    def get_results(self):

        return self.results

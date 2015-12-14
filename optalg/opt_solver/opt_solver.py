#****************************************************#
# This file is part of OPTALG.                       #
#                                                    #
# Copyright (c) 2015, Tomas Tinoco De Rubira.        #
#                                                    #
# OPTALG is released under the BSD 2-clause license. #
#****************************************************#

import numpy as np
from opt_solver_error import *

class OptSolver:

    # Constants
    STATUS_SOLVED = 'solved'
    STATUS_UNKNOWN = 'unknown'
    STATUS_ERROR = 'error'
    
    def __init__(self):
        """
        Optimization solver class.
        """
        
        #: Function data container.
        self.fdata = OptFuncData()
        
        #: Parameters dictionary.
        self.parameters = {}

        #: List of callback functions.
        self.callbacks = []

        #: List of termination conditions.
        self.terminations = []
        
        #: Information printer (function).
        self.info_printer = None

        # Other
        self.k = 0.
        self.x = None
        self.lam = None
        self.nu = None
        self.mu = None
        self.pi = None
        self.status = self.STATUS_UNKNOWN
        self.error_msg = ''              

        # Norms
        self.norminf = lambda x: np.linalg.norm(x,np.inf) if x.size else 0.
        self.norm2 = lambda x: np.linalg.norm(x,2)
        
    def add_callback(self,c):
        """
        Adds callback funtion to solver.
        
        Parameters
        ----------
        c : Function
        """
        
        self.callbacks.append(c)

    def add_termination(self,t):
        """
        Adds termination condition to solver.

        Parameters
        ----------
        t : Function
        """

        self.terminations.append(t)

    def get_error_msg(self):
        """
        Gets solver error message.
        
        Returns
        -------
        message : string
        """

        return self.error_msg
        
    def get_iterations(self):
        """
        Gets solver number of iterations.
        
        Returns
        -------
        iters : int
        """

        return self.k

    def get_status(self):
        """
        Gets solver status.
        
        Returns
        -------
        status : string
        """

        return self.status

    def get_primal_variables(self):
        """
        Gets solver optimization variables.

        Returns
        -------
        variables : ndarray
        """

        return self.x

    def get_dual_variables(self):
        """        
        Returns
        -------
        
        """
        
        return self.lam,self.nu,self.mu,self.pi

    def get_results(self):

        return {'status': self.status,
                'error_msg': self.error_msg,
                'k': self.k,
                'x': self.x,
                'lam': self.lam,
                'nu': self.nu,
                'mu': self.mu,
                'pi': self.pi}

    def is_status_solved(self):
        """
        Determines whether the solver solved the given problem.

        Returns
        -------
        flag : {``True``, ``False``}
        """

        return self.status == self.STATUS_SOLVED

    def line_search(self,x,p,F,GradF,func,smax=np.inf):
        """
        Finds steplength along search direction p that 
        satisfies the Wolfe conditions.
        
        Parameters
        ----------
        x : current point (ndarray)
        p : search direction (ndarray)
        F : function value at `x` (float)
        GradF : gradient of function at `x` (ndarray)
        func : function of `x` that returns function object with attributes `F` and `GradF` (function)
        smax : maximum allowed steplength (float)
           
        Returns
        -------
        s : stephlength that satisfies the Wolfe conditions (float).           
        """
        
        # Parameters of line search
        c1 = 1e-4
        c2 = 5e-1
        maxiter = 40

        # Initialize lower bound, upper bound and step
        l = 0.
        if 1. < smax:
            s = 1.
        else:
            s = smax
        u = np.NaN        

        phi = F
        dphi = np.dot(GradF,p)
        
        # Check that p is descent direction
        if dphi >= 0:
            raise OptSolverError_BadSearchDir(self)

        # Bisection
        for i in xrange(0,maxiter):
            
            xsp = x+s*p
            
            fdata = func(xsp)
            phis = fdata.F
            dphis = np.dot(fdata.GradF,p)
            
            if phis > phi + c1*s*dphi:
                u = s
            elif dphis > 0 and dphis > -c2*dphi:
                u = s
            elif dphis < 0 and -dphis > -c2*dphi:
                l = s
                if s >= smax:
                    return s,fdata
            else:
                return s,fdata

            if np.isnan(u):
                s = np.min([2.*s,smax])
            else:
                s = (l + u)/2.

        raise OptSolverError_LineSearch(self)

    def reset(self):
        """
        Resets solver data.
        """
        
        self.k = 0.
        self.x = None
        self.lam = None
        self.nu = None
        self.mu = None
        self.pi = None
        self.status = self.STATUS_UNKNOWN
        self.error_msg = ''

    def set_error_msg(self,msg):
        """
        Sets solver error message.
        
        Parameters
        ----------
        msg : string
        """

        self.error_msg = msg

    def set_info_printer(self,printer):
        """
        Sets function for printing algorithm progress.

        Parameters
        ----------
        printer : Function.
        """

        self.info_printer = printer

    def set_parameters(self,parameters):
        """
        Sets solver parameters.

        Parameters
        ----------
        parameters : dict
        """
        
        for key,value in parameters.items():
            if self.parameters.has_key(key):
                self.parameters[key] = value

    def set_status(self,status):
        """
        Sets solver status.

        Parameters
        ----------
        status : string
        """

        self.status = status

    def solve(self,problem):
        """
        Solves optimization problem.

        Parameters
        ----------
        problem : OptProblem
        """

        pass

class OptFuncData:
    """
    Optimization function data container.
    """

    pass
        
class OptTermination:
    """
    Optimization termination condition.
    """
    
    def __init__(self,func,msg):
        """
        Constructor.

        Parameters
        ----------
        func : Boolean function that takes solver and variabels as inputs
        msg : string
        """
        
        self.func = func
        self.msg = msg
        
    def __call__(self,solver):
        if self.func(solver):
            raise OptSolverError(solver,self.msg)

class OptCallback:
    """
    Optimization callback function.
    """
    
    def __init__(self,func):
        """
        Constructor.
        
        Parameters
        ----------
        func : Function that takes solver as input
        """

        self.func = func

    def __call__(self,solver):
        self.func(solver)

class OptPrinter:
    """
    Optimization information-printer function.
    """

    def __init__(self,func):
        """
        Constructor.
        
        Parameters
        ----------
        func : Function that takes solver as input
        """

        self.func = func
    
    def __call__(self,solver):
        self.func(solver)
#****************************************************#
# This file is part of OPTALG.                       #
#                                                    #
# Copyright (c) 2015-2016, Tomas Tinoco De Rubira.   #
#                                                    #
# OPTALG is released under the BSD 2-clause license. #
#****************************************************#

class StochProblemMS_Policy:
    """
    Operation policy for multi-stage stochatic
    optimization problem.
    """

    def __init__(self,problem,name='',data=None,construction_time=0.):
        """
        Operation policy for multistage stochastic
        optimization problem.
        
        Parameters
        ----------
        problem : StochProblemMS
        name : string
        data : Object
        construction_time : float (minutes)
        """

        self.name = name
        self.data = data
        self.problem = problem
        self.construction_time = construction_time

    def get_name(self):
        """
        Gets policy name.

        Return
        ------
        name : str
        """
        
        return self.name

    def get_problem(self):
        """
        Gets problem.

        Return
        ------
        problem : StochProblemMS
        """
        
        return self.problem

    def get_construction_time(self):
        """
        Gets construction time.

        Return
        ------
        time : float
        """

        return self.construction_time

    def apply(self,t,x_prev,Wt):
        """
        Applies operation policy at stage t
        given operation details of the previous stage
        and observations up to the current time.

        Parameters
        ----------
        t : int
        x_prev : vector
        Wt : list

        Returns
        -------
        x : vector
        """

        return None
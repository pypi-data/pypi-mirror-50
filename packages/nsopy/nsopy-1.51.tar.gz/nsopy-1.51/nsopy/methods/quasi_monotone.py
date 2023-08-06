from __future__ import division
import numpy as np
import copy

from nsopy.methods.base import SolutionMethod
from nsopy.observer_pattern import Observable
from nsopy.utils import invert_oracle_sense

METHOD_QUASI_MONOTONE_DEFAULT_GAMMA = 1.0
LARGE_VAL = 10000


class SGMDoubleSimpleAveraging(SolutionMethod, Observable):
    """ Implementation of "Subgradient Method with Double Simple Averaging", p.928.
    Yu. Nesterov , V. Shikhman, "Quasi-monotone Subgradient Methods for Nonsmooth Convex Minimization"
    Journal of Optimization Theory and Applications
    http://link.springer.com/article/10.1007/s10957-014-0677-5
    """
    def __init__(self, oracle, projection_function, dimension=0, gamma=METHOD_QUASI_MONOTONE_DEFAULT_GAMMA, sense='min'):
        super(SGMDoubleSimpleAveraging, self).__init__()

        self.desc = 'DSA, $\gamma = {}$'.format(gamma)
        self.oracle = oracle
        if sense == 'min':
            self.oracle = invert_oracle_sense(oracle)  # all methods have been coded to maximize the oracle model
        elif sense == 'max':
            self.oracle = oracle
        else:
            raise ValueError('Sense should be either "min" or "max"')
        self.projection_function = projection_function

        self.oracle_calls = 0
        self.iteration_number = 0

        if dimension == 0:
            self.lambda_k = self.projection_function(0)
            self.dimension = len(self.lambda_k)
        else:
            self.dimension = dimension
            self.lambda_k = self.projection_function(np.zeros(self.dimension, dtype=float))

        self.lambda_k = np.zeros(self.dimension, dtype=float)
        self.x_k = None
        self.diff_d_k = None
        self.d_k = -np.infty

        self.gamma = gamma
        self.s_k = np.zeros(self.dimension, dtype=float)  # this stores \sum_{k=0}^t diff_d_k

        # for record keeping
        self.method_name = 'DSA'
        self.parameter = gamma

    def dual_step(self):
        self.x_k, self.d_k, self.diff_d_k = self.oracle(self.lambda_k)
        self.oracle_calls += 1
        self.notify_observers()  # placed here to avoid mismatch between lambda_k and d_k

        self.s_k += self.diff_d_k
        lambda_k_plus = float(1.0)/float(self.gamma*np.sqrt(self.iteration_number+1)) * self.s_k
        lambda_k_plus = self.projection_function(lambda_k_plus)

        self.lambda_k = float(self.iteration_number+1)/float(self.iteration_number+2)*self.lambda_k \
                        + float(1.0)/float(self.iteration_number+2)*lambda_k_plus

        self.iteration_number += 1
        # self.notify_observers()


class SGMDoubleSimpleAveragingEntropy(SolutionMethod, Observable):
    """ Implementation of "Subgradient Method with Triple Averaging",
    p.930 of http://link.springer.com/article/10.1007/s10957-014-0677-5
    Variation of DSA with Entropy prox term.
    """
    def __init__(self, oracle, softmax_projection_function, dimension=0, SR=LARGE_VAL, gamma=METHOD_QUASI_MONOTONE_DEFAULT_GAMMA):
        super(SGMDoubleSimpleAveragingEntropy, self).__init__()

        self.desc = 'DSA Entropy, $\gamma = {}$'.format(gamma)
        self.oracle = oracle
        self.softmax_projection_function = softmax_projection_function

        self.oracle_calls = 0
        self.iteration_number = 0

        if dimension == 0:
            self.lambda_k = self.softmax_projection_function(0)
            self.dimension = len(self.lambda_k)
        else:
            self.dimension = dimension
            self.lambda_k = self.softmax_projection_function(np.zeros(self.dimension, dtype=float))

        self.lambda_k = np.zeros(self.dimension, dtype=float)
        self.x_k = None
        self.diff_d_k = None
        self.d_k = -np.infty

        self.gamma = gamma
        self.SR = SR
        self.s_k = np.zeros(self.dimension, dtype=float)  # this stores \sum_{k=0}^t diff_d_k

        # for record keeping
        self.method_name = 'DSA-Entropy'
        self.parameter = gamma

    def dual_step(self):
        self.x_k, self.d_k, self.diff_d_k = self.oracle(self.lambda_k)
        self.oracle_calls += 1
        self.notify_observers()  # placed here to avoid mismatch between lambda_k and d_k

        self.s_k += self.diff_d_k
        mu_k = float(self.SR) / float(self.gamma * np.sqrt(self.iteration_number + 1))
        psi_k_plus = mu_k * self.s_k
        lambda_k_plus = self.softmax_projection_function(psi_k_plus)

        self.lambda_k = float(self.iteration_number+1)/float(self.iteration_number+2)*self.lambda_k \
                        + float(1.0)/float(self.iteration_number+2)*lambda_k_plus
        self.iteration_number += 1
        # self.notify_observers()


class SGMTripleAveraging(SolutionMethod, Observable):
    """ Implementation of "Subgradient Method with Triple Averaging",
    p.930 of http://link.springer.com/article/10.1007/s10957-014-0677-5
    """
    def __init__(self, oracle, projection_function, dimension=0, variant=1, gamma=METHOD_QUASI_MONOTONE_DEFAULT_GAMMA, sense='min'):
        super(SGMTripleAveraging, self).__init__()

        self.desc = 'TA, $\gamma = {}$'.format(gamma)

        if sense == 'min':
            self.oracle = invert_oracle_sense(oracle)  # all methods have been coded to maximize the oracle model
        elif sense == 'max':
            self.oracle = oracle
        else:
            raise ValueError('Sense should be either "min" or "max"')
        self.projection_function = projection_function

        self.oracle_calls = 0
        self.iteration_number = 0
        self.gamma = gamma
        self.variant = variant

        self.d_k = 0
        if dimension == 0:
            self.lambda_k = self.projection_function(0)
            self.dimension = len(self.lambda_k)
        else:
            self.dimension = dimension
            self.lambda_k = self.projection_function(np.zeros(self.dimension, dtype=float))

        self.lambda_0 = copy.deepcopy(self.lambda_k)
        self.x_k = 0

        self.s_k = np.zeros(self.dimension, dtype=float)  # this stores \sum_{k=0}^t diff_d_k

        # for record keeping
        self.method_name = 'TA'
        self.parameter = gamma

    def dual_step(self):
        self.x_k, self.d_k, self.diff_d_k = self.oracle(self.lambda_k)
        self.oracle_calls += 1
        self.notify_observers()

        # step 1
        if self.variant == 1:
            self.desc = 'TA 1, $\gamma = {}$'.format(self.gamma)
            self.method_name = 'TA 1'
            self.s_k += self.diff_d_k
            gamma_t = self.gamma*np.sqrt(self.iteration_number+1)
            gamma_t_plus_1 = self.gamma*np.sqrt(self.iteration_number+2)
            tau_t = float(1)/float(self.iteration_number+2)

        elif self.variant == 2:
            self.desc = 'TA 2, $\gamma = {}$'.format(self.gamma)
            self.method_name = 'TA 2'
            self.s_k += (self.iteration_number+1)*self.diff_d_k
            # OLD Version: verbatim as in Paper
            # gamma_t = (self.iteration_number+1)**(float(3.0)/float(2.0))
            # gamma_t_plus_1 = (self.iteration_number+2)**(float(3.0)/float(2.0))
            # NEW Version: with tuning gamma
            gamma_t = self.gamma*(self.iteration_number+1)**(float(3.0)/float(2.0))
            gamma_t_plus_1 = self.gamma*(self.iteration_number+2)**(float(3.0)/float(2.0))
            tau_t = float(self.iteration_number+1)/float(sum([i for i in range(self.iteration_number+2)]))

        else:
            raise ValueError('Supported variants are 1: a_t = 1, gamma_t = gamma*sqrt(t+1) and '
                             '2: a_t = t, gamma_t = t^(3/2).')

        lambda_k_plus = float(1.0)/float(gamma_t) * self.s_k
        lambda_k_plus = self.projection_function(lambda_k_plus)

        # step 2
        lambda_k_hat = float(gamma_t)/float(gamma_t_plus_1) * lambda_k_plus \
                       + (1 - float(gamma_t)/float(gamma_t_plus_1))* self.lambda_0


        # step 4
        self.lambda_k = (1-tau_t)*self.lambda_k + tau_t*lambda_k_hat

        self.iteration_number += 1

# Generated with SMOP  0.41
from libsmop import *
# solvePhaseLamp.m

    ##                        solvePhaseLamp.m
    
    #  Implementation of the PhaseLamp algorithm. This algorithm iteratively
#  solves Phasemax. The algorithm terminates when the tolerance goes below
#  a specified threshold, or the number of iterations exceeds a specific
#  number of iterations, T. The Phasemax solver is implemented in the
#  solvePhaseMax.m function.
    
    
    ## I/O
#  Inputs:
#     A:    m x n matrix or a function handle to a method that
#           returns A*x.     
#     At:   The adjoint (transpose) of 'A'. If 'A' is a function handle, 'At'
#           must be provided.
#     b0:   m x 1 real,non-negative vector consists of all the measurements.
#     x0:   n x 1 vector. It is the initial guess of the unknown signal x.
#     opts: A struct consists of the options for the algorithm. For details,
#           see header in solvePhaseRetrieval.m or the User Guide.
    
    #     Note: When a function handle is used, the
#     value of 'At' (a function handle for the adjoint of 'A') must be 
#     supplied.
# 
#  Outputs:
#     sol:  n x 1 vector. It is the estimated signal.
#     outs: A struct consists of the convergence info. For details,
#           see header in solvePhaseRetrieval.m or the User Guide.
#
    
    ## Algorithm Description
#  The PhaseMax signal reconstruction problem is formulated as:
#         maximize <x0,x>
#         subject to |Ax|<b0 # <=
# 
#  This paper iteratively solves Phasemax. The algorithm terminates when
#  the tolerance goes beloe a specified threshold, or the number of
#  iterations exceeds a specific number of iterations, T.
    
    #  For a detailed explanation, see the PhaseLamp paper referenced below.
    
    ## References
#  Paper Title:   Phase Retrieval via Linear Programming: Fundamental
#                 Limits and Algorithmic Improvements.
#  arXiv Address: https://arxiv.org/abs/1710.05234
#  
# PhasePack by Rohan Chandra, Ziyuan Zhong, Justin Hontz, Val McCulloch,
# Christoph Studer, & Tom Goldstein 
# Copyright (c) University of Maryland, 2017
## ---------------------------------------------------------------------
    
    
@function
def solvePhaseLamp(A=None,At=None,b0=None,x0=None,opts=None,*args,**kwargs):
    varargin = solvePhaseLamp.varargin
    nargin = solvePhaseLamp.nargin

    T=10
# solvePhaseLamp.m:57
    
    eps=0.001
# solvePhaseLamp.m:58
    # Initial Iterate. Computed using one of the many initializer methods
# provided with Phasepack.
    xk_prev=copy(x0)
# solvePhaseLamp.m:61
    # Start the iteration process
    for i in arange(1,T).reshape(-1):
        if opts.verbose:
            fprintf('PhaseLamp iteration %d\n',i)
        # Running Phasemax in a loop. This command runs phasemax for the
    # current iteration.
        xk_next,outs=solvePhaseMax(A,At,b0,xk_prev,opts,nargout=2)
# solvePhaseLamp.m:71
        # current and next iterate is minimal.
        tol=norm(xk_next - xk_prev) / max(norm(xk_next),norm(xk_prev) + 1e-10)
# solvePhaseLamp.m:75
        if (tol < eps):
            break
        # Update the iterate
        xk_prev=copy(xk_next)
# solvePhaseLamp.m:81
    
    if opts.verbose:
        disp(concat(['Total iterations of PhaseLamp run: ',num2str(i)]))
    
    sol=copy(xk_next)
# solvePhaseLamp.m:88
    
    return sol,outs
    
if __name__ == '__main__':
    pass
    
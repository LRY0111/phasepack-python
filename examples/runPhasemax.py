# Generated with SMOP  0.41
from libsmop import *
# runPhasemax.m

    ##                   testPhaseMaxGaussian.m
    
    # This test file implements the Phasemax solver. The code builds
# a synthetic formulation of the Phase Retrieval problem, b = |Ax| and
# computes an estimate to x. The code finally plots a convergence curve
# and also makes a scatter plot of the true vs recovered solution.
    
    # PAPER TITLE:
#              PhaseMax: Convex Phase Retrieval via Basis Pursuit.
    
    # ARXIV LINK:
#              https://arxiv.org/abs/1610.07531
    
    # 1) Each test script starts out by defining the length of the unknown
# signal, n and the number of measurements, m. These mesurements can be
# made complex by setting the isComplex flag to be true.
    
    # 2) We then build the test problem by invoking the function
# 'buildTestProblem' which generates random gaussian measurements according
# to the user's choices in step(1). The function returns the measurement 
# matrix 'A', the true signal 'xt' and the measurements 'b0'.
    
    # 3) We set the options for the PR solver. For example, the maximum
# number of iterations, the tolerance value, the algorithm and initializer
# of choice. These options are controlled by setting the corresponding
# entries in the 'opts' struct.  Please see the user guide for a complete 
# list of options.
    
    # 4) We solve the phase retrieval problem by running the following line 
# of code:
#   >>  [x, outs, opts] = solvePhaseRetrieval(A, A', b0, n, opts)
# This solves the problem using the algorithm and initialization scheme
# specified by the user in the struct 'opts'.
    
    # 5) Determine the optimal phase rotation so that the recovered solution
# matches the true solution as well as possible.
    
    # 6) Report the relative reconstruction error. Plot residuals (a measure
# of error) against the number of iterations and plot the real part of the 
# recovered signal against the real part of the original signal.
    
    # PhasePack by Rohan Chandra, Ziyuan Zhong, Justin Hontz, Val McCulloch,
# Christoph Studer, & Tom Goldstein 
# Copyright (c) University of Maryland, 2017
    
    ## -----------------------------START-----------------------------------
    
    clc
    clear
    close_('all')
    n=256
# runPhasemax.m:57
    
    m=dot(7,n)
# runPhasemax.m:58
    
    isComplex=copy(true)
# runPhasemax.m:59
    
    ##  Build a random test problem
    fprintf('Building test problem...\n')
    A,xt,b0=buildTestProblem(m,n,isComplex,nargout=3)
# runPhasemax.m:63
    # Use this line instead to run on Transmission Matrix dataset
#[A, b0, xt, plotter] = experimentTransMatrixWithSynthData(n, m, []);
    
    # Options
    opts=copy(struct)
# runPhasemax.m:69
    opts.initMethod = copy('optimal')
# runPhasemax.m:70
    opts.algorithm = copy('PhaseMax')
# runPhasemax.m:71
    opts.isComplex = copy(isComplex)
# runPhasemax.m:72
    opts.maxIters = copy(10000)
# runPhasemax.m:73
    opts.tol = copy(1e-06)
# runPhasemax.m:74
    opts.verbose = copy(1)
# runPhasemax.m:75
    ## Try to recover x
    fprintf('Running algorithm...\n')
    x,outs,opts=solvePhaseRetrieval(A,A.T,b0,n,opts,nargout=3)
# runPhasemax.m:79
    ## Determine the optimal phase rotation so that the recovered solution
#  matches the true solution as well as possible.
    alpha=(dot(x.T,xt)) / (dot(x.T,x))
# runPhasemax.m:83
    x=dot(alpha,x)
# runPhasemax.m:84
    ## Determine the relative reconstruction error.  If the true signal was 
#  recovered, the error should be very small - on the order of the numerical
#  accuracy of the solver.
    reconError=norm(xt - x) / norm(xt)
# runPhasemax.m:89
    fprintf('relative recon error = %d\n',reconError)
    # Plot a graph of error(definition depends on if opts.xt is provided) versus
# the number of iterations.
    plotErrorConvergence(outs,opts)
    # Plot a graph of the recovered signal x against the true signal xt.
    plotRecoveredVSOriginal(x,xt)
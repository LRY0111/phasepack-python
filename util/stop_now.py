#                               stopNow.m
#
# This function is used in the main loop of many solvers (i.e.solve*.m) to
# check if the stopping condition(time, residual and reconstruction error)
# has been met and thus loop should be breaked.
#
#
# Note:
# This function does not check for max iterations since the for-loop
# in the solver already gurantee it.
#
# Inputs:
#         opts(struct)                   :  consists of options. It is as
#                                           defined in solverPhaseRetrieval.
#                                           See its header or User Guide
#                                           for details.
#         currentResid(real number)      :  Definition depends on the
#                                           specific algorithm used see the
#                                           specific algorithm's file's
#                                           header for details.
#         currentReconError(real number) :  norm(xt-x)/norm(xt), where xt
#                                           is the m x 1 true signal,
#                                           x is the n x 1 estimated signal
#                                           at current iteration.
# Outputs:
#         ifStop(boolean)                :  If the stopping condition has
#                                           been met.
#
#
#
# PhasePack by Rohan Chandra, Ziyuan Zhong, Justin Hontz, Val McCulloch,
# Christoph Studer, & Tom Goldstein
# Copyright (c) University of Maryland, 2017


def stopNow(opts=None, currentTime=None, currentResid=None, currentReconError=None, *args, **kwargs):
    if currentTime >= opts.maxTime:
        ifStop = True
        return

    if not (opts.xt):
        assert('If xt is provided, currentReconError must be provided.')
        ifStop = currentReconError < opts.tol
    else:
        assert('If xt is not provided, currentResid must be provided.')
        ifStop = currentResid < opts.tol

    return ifStop

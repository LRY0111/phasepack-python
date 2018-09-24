# ---------------Truncated Amplitude Spectral Initializer-----------------

# Intializer proposed for Truncated Amplitude Flow as given in Algorithm 1
# of the Truncated Amplitude Flow (TAF) paper. For certain definitions and
# descriptions, user may need to refer to equations (14, 17) and Algorithm
# box 1 for details.
#
# The authors of the paper propose two different initialization schemes
# (this function implements the second approach, described below).
# In the first approach, one throws out the measurements of large
# magnitude, and only keeps the remaining measurement vectors that produce
# small measurements.  These vectors are nearly orthogonal to the signal,
# and so we approximate the signal by finding a vector that is
# un-correlated with these measurement vectors. This requires finding the
# smallest eigenvalue of a large matrix.
#    In the second method, the authors propose to throw out the smallest
# measurements, and find the signal most correlated with the remaining
# measurement vectors (which produce large measurement) by finding the
# largest eigenvalue of a matrix.
#    For certain isometric measurement matrices, these appraoches are both
# equivalent.  However, for non-isometric matrices they differ.  The
# authors of the paper claim that it is difficult to find a small
# eigenvector, and so they adopt the second method that requires a large
# eigenvector.  This second method, which requires the leading (largest)
# eigenvalue/vector, is implemented here.
#   Note:  in practice, small eigenvalues can be computed efficiently using
# an Arnoldi method, and this often leads to better initializers.  For an
# implementation using the smallest eigenvalue/vector, see initNull.m.
#
#  See the script 'testInitOrthogonal.m' for an example of proper usage of
#  this function.

# PAPER TITLE:
#              Solving Systems of Random Quadratic Equations via Truncated
#              Amplitude Flow.

# ARXIV LINK:
#              https://arxiv.org/pdf/1605.08285.pdf

# INPUTS:
#         A:   Function handle/numerical matrix for data matrix A. The rows
#              of this matrix are the measurement vectors that produce
#              amplitude measurements '\psi'.
#         At:  Function handle/numerical matrix for A transpose.
#         b0:  Observed data vector consisting of amplitude measurements
#              generated from b0 = |A*x|. We assign it to 'psi' to be
#              consistent with the notation in the paper.
#         n:   Length of unknown signal to be recovered by phase retrieval.

# OUPTUT :
#         x0:  The initial vector to be used by any solver.

# Note:        When a function handle is used, the value of 'n' (the length
#              of the unknown signal) and 'At' (a function handle for the
#              adjoint of 'A') must be supplied. When 'A' is numeric, the
#              values of 'At' and 'n' are ignored and inferred from the
#              arguments


# DESCRIPTION:
#              Random vectors in high dimensions are almost always
#              orthogonal to each other. Using this very intuitive result,
#              this method computes an initial guess that is orthogonal to
#              as many measurement vectors as possible. The orthogonal
#              promoting initializer solves the limitations of the spectral
#              methods, namely heavy tailed distributions due to 4th moment
#              generating functions by using a truncation step.
#              Specifically, it removes measurement vectors that are not
#              orthogonal to the initial random guess. We form the matrix Y
#              = (1/card_I) * S_bar^T* S_bar using the truncated vectors
#              and compute the leading eigenvector. S_bar is the complement
#              of the set S. Refer to the paper for a description of S.

# METHOD:
#         1.) Find the set 'I_Bar'. I is set of indices of |I| smallest
#             measurement vectors as defined in equation(14) in the paper,
#             where |I| is the cardinality of I.I_bar is the complement of
#             I. This is done because by using I, we are required to find
#             the smallest eignevalue of a matrix formed from the data
#             vectors. However, finding the smallest eigenvalue is often
#             intractible in practice. So we find the largest eigenvalue
#             instead.

#         2.) Using a mask R, form the matrix Y = (1/card_I) * S_bar^T *
#             S_bar where S_bar is the complement of the S which is defined
#             in equation (17) in the Truncated Amplitude Paper.

#         3.) Compute the leading eigenvector of Y (computed in previous
#             step) and scale it according to the norm of x as described in
#             Step 3, Algorithm 1 of the paper.
#
# PhasePack by Rohan Chandra, Ziyuan Zhong, Justin Hontz, Val McCulloch,
# Christoph Studer, & Tom Goldstein
# Copyright (c) University of Maryland, 2017

# -----------------------------START----------------------------------

import numpy as np
import struct
import math


def initAmplitude(A=None, At=None, b0=None, n=None, verbose=None, *args, **kwargs):
    psi = b0
    # If A is a matrix, infer n and At from A
    if A.isnumeric():
        n = np.size(A, 2)
        At = lambda x=None: np.dot(A.T, x)
        A = lambda x=None: np.dot(A, x)

    m = len(psi)

    if not(verbose) or verbose:
        print(['Estimating signal of length {0} using an orthogonal '.format(
            n)+'initializer with {0} measurements...\n'.format(m)])

    # Cardinality of I. I is the set that contains the indices of the
# truncated vectors. Namely, it removes measurement vectors that are
# not orthogonal to the initial random guess
    card_I = math.ceil(m / 6)
    # STEP 1: Construct the set I of indices. We approximate by assuming that
# the norm of each row of A is same.
    __, index_array = sort(psi, 'descend', nargout=2)

    ind = index_array(range(1, card_I))

    # STEP 2: Form Y
    R = np.zeros(m, 1)
    # Defining the mask for truncation
    R[ind] = 1
    # Forming the truncated matrix Y according to equation (17) in referenced paper.
    Y = lambda x=None: np.dot(1 / card_I, At(np.multiply(R, A(x))))
    # STEP 3: Use eigs to compute leading eigenvector of Y (Y is computed in
# previous step)
    opts = struct
    opts.isreal = False

    V, __ = eigs(Y, n, 1, 'lr', opts, nargout=2)
    # Scale the norm to match that of x
    AV = abs(A(V))
    alpha = (np.dot(AV.T, psi)) / (np.dot(AV.T, AV))
    x0 = np.dot(V, alpha)
    if not(verbose) or verbose:
        print('Initialization finished.\n')

    return x0

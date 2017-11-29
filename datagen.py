import numpy
import random
from typing import List

# utility to permute a matrix (randomly if necessary)
def shuffleMatrix(mat : numpy.ndarray, permutation : List=[]):
    """
    :param mat: a square numpy matrix to permute
    :param permutation: a list of where each column/row comes from (zero len to generate random)
    :return:
    """
    msize = len(mat)
    if msize != len(mat[0]):
        raise ValueError("Attempt to Permute Non-Square Matrix")
    if len(permutation)==0:
        permutation = [i for i in range(msize)]
        random.shuffle(permutation)
    result = numpy.zeros_like(mat)
    for i in range(msize):
        for j in range(msize):
            result[i,j] = mat[permutation[i],permutation[j]]
    return result

# generate a purely random communication network
def randomNet(msize:int, nmessages:int):
    mat = numpy.zeros( (msize,msize) )
    for c in range(nmessages):
        fr = random.randint(0,msize-1)
        # make sure that to is not the same as from
        to = random.randint(0,msize-2)
        if to>=fr: to += 1
        mat[fr,to] += 1
    return mat

# generate a random net, with a given distribution
def randomDist(distrib:List, nmessages:int):
    msize = len(distrib)
    mat = numpy.zeros( (msize,msize) )
    for fr in random.choices([i for i in range(msize)],weights=distrib,k=nmessages):
        # make sure that to is not the same as from
        to = random.randint(0,msize-2)
        if to>=fr: to += 1
        mat[fr,to] += 1
    return mat


# a random net that is a little "cliquy"
# random process - but a higher chance that a message is within a clique


# a random net that is "hierarchical"
# each node has a list of children - 3 types of messages (random, downstream, upstream)

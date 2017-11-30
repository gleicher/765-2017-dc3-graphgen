import numpy
import random
from typing import List,Union,Tuple

# write a set of matrices to a file
# given a list of either:
# (1) just matrices
# (2) tuples of (name,matrix, (optional) node names)
# if name or node names aren't provided they are given the default values
def writeMatrices(filename : str, data : List[Union[numpy.ndarray,Tuple]]):
    with open(filename,"w") as fo:
        for i,md in enumerate(data):
            mat = md[1] if type(md)==tuple else md
            size = len(md)
            name = md[0] if type(md)==tuple else "Group {}".format(i)
            names = md[2] if type(md)==tuple and len(md)>2 else ["{:c}".format(j+65) for j in range(size)]
            fo.write("{} {}\n".format(size,name))
            for t in zip(names,mat):
                string = t[0]
                for v in t[1]:
                    string += ", " + str(v)
                fo.write(string + "\n")

# read in a file with a bunch of matrices
# returns a list of tuples: (name, matrix, nodenames)
def readMatrices(filename):
    mats = []
    mat = False
    name = False
    names = []

    def addCurrentMat():
        nonlocal name,mat,names
        if name != False:
            mats.append((name, mat, names))
            mat = False
            name = False
            names = []

    with open(filename) as fi:
        # keep track of the matrix we're in the process of reading, write it when
        # the next one starts (or we end)

        for row in fi:
            cspl = row.lstrip().rstrip().split(",")
            if (len(cspl))==1:
                addCurrentMat()
                sspl = row.rstrip().lstrip().split(" ")
                size = int(sspl[0])
                name = " ".join(sspl[1:])
                mat = numpy.zeros((size,size))
            else:
                r = len(names)
                for i,v in enumerate(cspl[1:]):
                    mat[r,i] = float(v)
                names.append(cspl[0])
        addCurrentMat()
        return mats



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
# either give a size, or a list of weights
def randomNet(spec:Union[int,List[float]], nmessages:int):
    ## setup weights and size
    try:
        # if this is an integer, then make up the weights
        msize = int(spec)
        weights = [1] * msize
    except TypeError:
        # it must be a list of weights
        weights = spec
        msize = len(spec)
    ## actually create the matrix by sampling
    mat = numpy.zeros( (msize,msize) )
    for fr in random.choices([i for i in range(msize)],weights=weights,k=nmessages):
        # make sure that to is not the same as from
        to = random.randint(0,msize-2)
        if to>=fr: to += 1
        mat[fr,to] += 1
    return mat


# a random net that is a little "cliquy"
# random process - but a higher chance that a message is within a clique


# a random net that is "hierarchical"
# each node has a list of children - 3 types of messages (random, downstream, upstream)


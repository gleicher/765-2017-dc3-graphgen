"""
Code for generating example data for Design Challenge 3 for
CS765 Data Visualization - Fall, 2017
http://graphics.cs.wisc.edu/WP/vis17/2017/11/25/dc3-design-challenge-3-compare-networks/

Written hastily by Mike Gleicher in November 2017

This file has code to read and write sets of matrices (that represent networks)
which may be useful in projects. It also has code to generate random networks
to test out visualizations.

Students may use portions of this code, providing they give proper attribution.

This code was written using python 3.6 and the numpy library
"""

import numpy
import random
from typing import List,Union,Tuple

# write a set of matrices to a file
# given a list of either:
# (1) just matrices
# (2) tuples of (name,matrix, (optional) node names)
# if name or node names aren't provided they are given the default values
def nameMaker(num:int):
    return "{:c}{:c}".format(65+int(num/26),65+int(num%26),num)
def writeMatrices(filename : str, data : List[Union[numpy.ndarray,Tuple]]):
    with open(filename,"w") as fo:
        gcount = 0
        for i,md in enumerate(data):
            mat = md[1] if type(md)==tuple else md
            size = len(mat)
            name = md[0] if type(md)==tuple else "Group {}".format(i)
            names = md[2] if type(md)==tuple and len(md)>2 else [nameMaker(j+gcount) for j in range(size)]
            gcount += size
            fo.write("{} {}\n".format(size,name))
            for t in zip(names,mat):
                string = t[0]
                for v in t[1]:
                    string += ", " + str(v)
                fo.write(string + "\n")

# read in a file with a bunch of matrices
# returns a list of tuples: (name, matrix, nodenames)
def readMatrices(filename):
    # keep track of the matrix we're in the process of reading, write it when
    # the next one starts (or we end)
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
    # the actual reading loop
    with open(filename) as fi:
        # process each row - if it's the beginning of a new matrix, act accordingly
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

# helper function - which is used by randomNet
# figure out which partition a node is in
def partitionOf(node, msize, partitions):
    """
    figure out which partition a node is in - returns the beginning and end of the partition
    useful in randomNet
    :param node:
    :param msize:
    :param partitions:
    :return:
    """
    # naively make equal size partitions - and one big one at the end
    psize = int(msize/partitions)
    pindex = int(node/psize)
    # rather than the little parition at the end, we add it to the last one
    if pindex>=partitions: pindex=partitions-1
    # the last partition goes to the end
    if pindex==partitions-1:
        return (pindex*psize, msize-1)
    else:
        return (pindex*psize, (pindex+1)*psize-1)


# generate a purely random communication network
# either give a size, or a list of weights
def randomNet(spec:Union[int,List[float]], nmessages:int,
              partitions:int=0, partitionProb:float=.8):
    """
    This is the function that actually generates a random network (the matrix of message counts)

    :param spec: the size of the matrix - either an integer, or a list of weights.
        If an integer is given, it is the number of nodes, given equal weight.
        If a list is given, the length is the number of nodes, and the values are the weights for the distribution of sending.
    :param nmessages:  the total number of messages
    :param partitions: the number of partitions in the network - use 0 for a whole partition (1 should do the same thing)
    :param partitionProb: the probability of a message being sent within the partition.
        If 1, all messages are within the partitions (the matrix will be block diagonal).
        If a message is not designated as within the partition, it still may end up going to
        a member of the partition.
    :return: the nxn matrix of counts
    """
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
    # generate the from nodes randomly
    for fr in random.choices([i for i in range(msize)],weights=weights,k=nmessages):
        # pick a "to" node by finding the range that the node can be in
        # (pi to pe, inclusive) - this allows us to do partitioning
        if partitions>0 and random.random()<partitionProb:
            pi,pe = partitionOf(fr,msize,partitions)
        else:
            pi,pe = 0,msize-1
        # make sure that to is not the same as from - shrink the partition and stretch it
        # around from
        to = random.randint(pi,pe-1)
        if to>=fr: to += 1
        mat[fr,to] += 1
    return mat

def addChain(matOrInt : Union[numpy.ndarray,int],
             forward=(50,70),backwards=(30,40),
             scramble=True):
    """
    Adds a "chain" (a link where person 1 sends to 2, 2 sends to 3, ...) to a network
    Either pass it a network (it adds to it), or an integer (creates a zero network)

    :param matOrInt: matrix to add to, or integer for matrix size
    :param forward: range of messages to add in the forward direction
    :param backwards: range of messages to ad in the reverse direction
    :param scramble: do a random order
    :return: the matrix passed in (or a new one, if an int was passed in)
    """
    if type(matOrInt) == int:
        matOrInt = numpy.zeros((matOrInt,matOrInt))
    size = len(matOrInt)
    index = [i for i in range(size)]
    if scramble:
        random.shuffle(index)
    for i in range(size-1):
        fr = index[i]
        to = index[i+1]
        matOrInt[fr,to] += random.randint(forward[0],forward[1])
        matOrInt[to,fr] += random.randint(backwards[0],backwards[1])
    return matOrInt


# a random net that is "hierarchical"
# each node has a list of children - 3 types of messages (random, downstream, upstream)

### generate the example files
def genExamples():
    writeMatrices("Examples/01-simplest-6x6.txt",
                  [("Random 1",randomNet(6,1000)),
                   ("Random 2",randomNet(6,1500)),
                   ("Random 3",randomNet(6,2000))])
    writeMatrices("Examples/02-weighted-6x6.txt",
                  [("Weighted 1", randomNet([10, 1, 1, 1, 1, 1], 1000)),
                   ("Weighted 2", randomNet([10,10, 1, 1, 1, 1], 1500)),
                   ("Weighted 3", randomNet([10,10,10, 1, 1, 1], 1500))
                  ])
    writeMatrices("Examples/03-varied-67.txt",
                  [("Unweighted 6", randomNet([ 1, 1, 1, 1, 1, 1], 1500)),
                   ("Weighted 6-1", randomNet([10,10, 1, 1, 1, 1], 1500)),
                   ("Weighted 6-2", randomNet([ 1, 1,10, 1,10, 1], 1500)),
                   ("Unweighted 7", randomNet([1, 1, 1, 1, 1, 1, 1], 1500)),
                   ("Weighted 6-1", randomNet([1,10,10, 1, 1, 1, 1], 1500)),
                   ("Weighted 6-2", randomNet([1, 1, 1,10, 1,10, 1], 1500)),
                  ])
    writeMatrices("Examples/04-partitioned-6.txt",
                  [
                      ("Non Part", randomNet(6,1500)),
                      ("2 part 1", randomNet(6,1500,2)),
                      ("2 part 2", shuffleMatrix(randomNet(6,1500,3))),
                      ("3 part 1", randomNet(6, 1500, 2)),
                      ("3 part 2", shuffleMatrix(randomNet(6, 1500, 3))),
                  ])

def genPartExamples():
    def genPartLevels(size,nlinks,nparts=[3],probs=[1,.8,.5,.2], repeats=1):
        mats = []
        for n in nparts:
            for p in probs:
                mats.append(("N({:d}) P({}) - 0".format(n,p), randomNet(size, nlinks, n, p)))
                for r in range(repeats):
                    mats.append(("N({:d}) P({}) - {:d}".format(n,p,r+1), shuffleMatrix(randomNet(size, nlinks, n, p))))
        return mats

    writeMatrices("Examples/05-partitioned-9-wt.txt", genPartLevels(9,2500,nparts=[3],repeats=1))
    writeMatrices("Examples/06-partitioned-12-wt.txt",genPartLevels(12,3200,nparts=[3,4],repeats=1))
    writeMatrices("Examples/07-paritions-9.txt",genPartLevels(9,2500,nparts=[2,3],probs=[.2,.7]))
    writeMatrices("Examples/08-paritions-12.txt",genPartLevels(12,3500,nparts=[3,4],probs=[.2,.7]))

def genChainExamples():
    writeMatrices("Examples/11-chains-simple7s.txt",
                  [
                      ("chain 7 - not scrambled", addChain(7,scramble=False)),
                      ("chain 7", addChain(7)),
                      ("another chain 7",addChain(7)),
                      ("chain 7 over noise - not scrambled", addChain(randomNet(7,700),scramble=False)),
                      ("chain 7 over noise", addChain(randomNet(7, 700))),
                      ("another chain 7 over noise", addChain(randomNet(7, 700)))
                  ])
    writeMatrices("Examples/12-chain-partition-7.txt",
                  [
                      ("chain + partition - clean",addChain(randomNet(7,700,2,1),scramble=False)),
                      ("chain + partition - clean+scramble",shuffleMatrix(addChain(randomNet(7,700,2,1)))),
                      ("chain + partition - scrambled chain",
                        addChain(randomNet(7,700,2,1))),
                      ("chain + partition - scrambled both",
                        addChain(shuffleMatrix(randomNet(7,700,2,1)))),
                      ("chain + partition - mixed",
                       addChain(shuffleMatrix(randomNet(7, 700, 2, .7)))),
                      ("chain + partition - mixed",
                       addChain(shuffleMatrix(randomNet(7, 700, 2, .7))))
                  ])
    writeMatrices("Examples/13-chain-partition-varied.txt",
                  [
                      ("one", addChain(randomNet(9,1400,2,.7))),
                      ("two", addChain(randomNet(9,1400, 2, .5))),
                      ("three", addChain(randomNet(9, 1400, 3, .7))),
                      ("four", addChain(randomNet(9, 1400, 3, .5))),
                      ("one", addChain(randomNet(8, 1200, 2, .7))),
                      ("two", addChain(randomNet(8, 1200, 2, .5))),
                      ("three", addChain(randomNet(8, 1200, 3, .7))),
                      ("four", addChain(randomNet(8, 1200, 3, .5))),

                  ])
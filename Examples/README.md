# Example Data for CS765 Design Challenge 3 - Network Comparison

This is example outputs from the random data generator. It is provided in case you don't want to run the program yourself
(which is understandable, since it requires a non-standard version of Python).

Each file contains a set of networks you can use for testing. They are numbered in a rough order of challenging-ness.

Note: the nodes in each network are meant to be different (e.g., the "A" node in network 1 is not the same "A" as in
network 2). Nodes within a file should all have unique names (but if they don't, assume that each network is different).

All these matrices are generated using the sample code.

The "partitioned" networks have strong subgroups (most messages stay within the subgroups).
For the examples (5-7, although 7 is duplicated), each matrix is described with 2 numbers:
n (the number of partitions) and p (the probability that a message stays within the partition vs. being to any other node).
A third number distinguishes between repeats of the same pattern.

The "chain" networks have a message chain (A sends messages to B, B to C, etc.).
This gives another pattern to mix in so you have something to find/compare.

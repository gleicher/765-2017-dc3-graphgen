# 765-2017-dc3-graphgen

# Sample Data Generator for CS765 Design Challenge 3: Small Network Comparison

This project was created by Michael Gleicher in November, 2017 to provide sample data for
students building projects for the project in CS765 (Data Visualization).

The project is described on the [course web site](http://graphics.cs.wisc.edu/WP/vis17/2017/11/25/dc3-design-challenge-3-compare-networks/).

Students are free to use this in their projects, if they give proper attribution.

In addition to code that generates random networks to compare and visualize, it also has a python
parser for the required data file format. 

The Examples subdirectory has a bunch of pre-computed network sets (if you want data, but don't want to run the program).

The program is written in Python 3.6.

## How the random networks are generated

The process for generating the random networks is simple, and has a few tweaks to generate interesting effects to see.

A network is defined by the number of nodes (people), and the number of total messages. 
For each message, a sender is sender is selected at random.
Then a recipient is selected at random.
The distribution of choice of sender can be given (otherwise it is uniform).
To simulate "partitioned" networks, the choice of recipient can be conditioned on the partition the sender is in.
If the network is partitioned, with some probability, the sender will choose a recipient in their partition
(otherwise they will choose randomly from all others, which may or may not be someone in their partition).

A message "chain" can be added (where person A sends to B sends to C) - to give another
pattern to spot / compare. 

In the future, other effects (like hierarchies) may be modeled.

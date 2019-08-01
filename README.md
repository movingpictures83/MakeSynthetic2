# MakeSynthetic2
# Language: Python
# Input: TXT (key-value pairs)
# Output: GML (synthetic network with these properties) 
# Tested with: PluMA 1.0, Python 3.6

PluMA plugin to build a synthetic network.  This was constructed
as a 'sequel' to the MakeSynthetic plugin, accounting for driver nodes,
hubs, and noise.

The input file is a simple text file with lines containing a keyword,
some whitespace, and a value.  Keywords understood by this plugin:

numclubs: The number of tightly connected components (positive edges).
          Each club will also have one 'driver' node, given higher edge weights
maxsize: Maximum possible size of any club
minsize: Minimum possible size of any club
pcthubs: Used to compute the number of hub nodes, as a percentage of the size
         of the largest club.  For example, if pcthubs=0.5 and the largest club
         is 20 nodes, there will be 10 hub nodes in the network
pctnoise: Used to compute the number of noisy edges to add, as a percentage
          of the number of nodes
numrivalclubs: Number of clubs that are "rivals", having lots of negative edges
               between them.  Not to exceed numclubs


Output is a synthetic network in the Graph Modeling Language (GML).
Weights are assigned randomly, within the following ranges:

Nodes within a social club: [0.75 - 1)
Edges with a common enemy: (-1 - 0.75]
Nodes between rival clubs: [-0.5 - 0]
Noise: [0 - 0.5]


import matplotlib.pyplot as plt
import numpy as np
import sys
from matplotlib import collections as mc

###################################################
###             QUESTION 2: QUADTREES           ###
###                                             ###
### Generating random data based on user inputs ###
###################################################

print "\n\nNumber n of random 2-dimensional data points:\n"
n = raw_input()
try:
    n = int(n)
except ValueError:
    sys.exit("Bad n, must be integer")

features = []

i = 0
while i < n:
    features.append([np.random.uniform(-1, 1), np.random.uniform(-1, 1)])
    i += 1

print "\nThreshold k for each quadrant:\n"
k = raw_input()
try:
    globalk = int(k)
except ValueError:
    sys.exit("Bad k, must be integer")

if globalk < 1 or n < 1:
    sys.exit("Bad inputs: k, n must be integers > 0")


################################################
### Building Classes for Quadtree generation ###
################################################

class QuadList:
    def __init__(self):
        self.allQuads = []

class Quad:
    def __init__(self, xmin, xmax, ymin, ymax, data, k, depth):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.isLeaf = 1
        self.children = []
        self.data = data
        self.k = k
        self.depth = depth

    def CountChildren(self):
        for datapoint in self.data:
            if datapoint[0] > self.xmin and datapoint[0] < self.xmax and datapoint[1] > self.ymin and datapoint[1] < self.ymax:
                self.children.append(datapoint)
        return len(self.children)

    def Split(self):
        self.isLeaf = 0
        self.branches = []
        self.branches.append(Quad(self.xmin, (self.xmax + self.xmin)/2.0, self.ymin, (self.ymax + self.ymin)/2.0, self.children, globalk, self.depth+1))
        self.branches.append(Quad(self.xmin, (self.xmax + self.xmin)/2.0, (self.ymax + self.ymin)/2.0, self.ymax, self.children, globalk, self.depth+1))
        self.branches.append(Quad((self.xmax + self.xmin)/2.0, self.xmax, self.ymin, (self.ymax + self.ymin)/2.0, self.children, globalk, self.depth+1))
        self.branches.append(Quad((self.xmax + self.xmin)/2.0, self.xmax, (self.ymax + self.ymin)/2.0, self.ymax, self.children, globalk, self.depth+1))
        return self.branches

    def Recurse(self, quadlist):
        if self.CountChildren() > self.k:
            self.isLeaf = 0
            self.Split()
            for subQuad in self.branches:
                subQuad.Recurse(quadlist)
        if self.isLeaf == 1:
            quadlist.allQuads.append(Quad(self.xmin, self.xmax, self.ymin, self.ymax, None, None, self.depth))


###########################################################################
### Using Quad Class and Recurse function to build all Quadtree brances ###
###########################################################################


finalQuads = QuadList()
startingQuad = Quad(-1, 1, -1, 1, features, globalk, 0)
startingQuad.Recurse(finalQuads)

print "\n\nCreated %d total quadtree segments\n" % (len(finalQuads.allQuads))

############################################
### Determining the "most dence quadrant ###
############################################
# Density of quad space determined by max  #
# 'depth' of quad - how many branches down #
# the tree the segment is. This is also    #
# going to represent the smallest square   #
# when graphing all quads and data points. #
############################################

sortedQuads = sorted(finalQuads.allQuads, key= lambda quad: quad.depth, reverse= True)
dense = sortedQuads[0]

area = (dense.xmax - dense.xmin) * (dense.ymax - dense.ymin)

print "'Smallest' quadree has area %e units-squared" % (area)

###########################################
### Plotting the Quadtree & Data Points ###
###########################################

quadlines = []
color = np.array([(1, 0, 0, 1)])

for quad in finalQuads.allQuads:
    quadlines.append([(quad.xmin, quad.ymin),(quad.xmin, quad.ymax)])
    quadlines.append([(quad.xmin, quad.ymin),(quad.xmax, quad.ymin)])
    quadlines.append([(quad.xmin, quad.ymax),(quad.xmax, quad.ymax)])
    quadlines.append([(quad.xmax, quad.ymin),(quad.xmax, quad.ymax)])

collection = mc.LineCollection(quadlines, colors= color, linewidths= 1)
ax = plt.axes()
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

ax.add_collection(collection)

X = []
Y = []

for data in features:
    X.append(data[0])
    Y.append(data[1])
plt.plot(X, Y, 'bo')

plt.show()


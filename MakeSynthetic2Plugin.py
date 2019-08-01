# TMC created this script on 7/2/15
# Purpose: Generate synthetic networks
# Intention is to produce examples that demonstrate the advantages
# of our approach (ATria) over others.
# Thus, you can specify the number of social clubs you want,
# minimum and maximum size, number of rival clubs you want,
# number of common enemies you want, and the amount of noise.
# At the moment noise just produces green edges, red edges are thus
# assumed to be predefined.

# Also specify the name.  The file created will appear in 
# (name)/(name).gml.  We use GML so that it can be easily analyzed by Cytoscape.

# Correlation Values for:
# Nodes within a social club: [0.75 - 1)
# Edges with a common enemy: (-1 - 0.75]
# Nodes between rival clubs: [-0.5 - 0]
# Noise: [0 - 0.5]

# hubs and noise are percentages.
# The amount of hub nodes will be equal to that percentage times the size of the largest club
# The amount of noise will be equal to that percentage times the number of nodes (i.e. if the graph
# has 100 nodes, there will be 50 edges that are random, with lower correlations [0 - 0.5]
import numpy
import math
import random
import sys
random.seed(1234)

class MakeSynthetic2Plugin: 
   def input(self, filename):
      myfile = open(filename, 'r')
      self.params = dict()
      for line in myfile:
         keyword, value = line.split()
         if keyword.startswith('pct'):
            self.params[keyword] = float(value)
         else: 
            self.params[keyword] = int(value)
      self.params['numdrivers'] = self.params['numclubs'] - self.params['numcommonenemies']
##############################
# Parameters
#numclubs = 5
#maxsize = 20
#minsize = 16
#pcthubs = 0.5
#pctnoise = 0.0
#numrivalclubs = 0
#numcommonenemies = 0
##############################

#numdrivers = numclubs - numcommonenemies
   def run(self):
      ####################################################
      # Determine the size of each club first.
      clubsizes = numpy.zeros([self.params['numclubs']])
      for i in range(self.params['numclubs']):
         clubsizes[i] = random.randint(self.params['minsize'], self.params['maxsize'])
      ####################################################

      ####################################################
      # Now compute n, the total number of nodes
      #
      # First, number of hubs
      numhubs = int(round(self.params['pcthubs'] * max(clubsizes)))
      #print type(int(sum(clubsizes)))
      #print type(int(numhubs))
      self.n = int(int(sum(clubsizes)) + int(numhubs))
      ####################################################

      ####################################################
      # Obtain the correct number of nodes
      # Partition them into clubs, hubs and common enemies
      # We can just do this linearly
      #
      nodes = range(0, self.n)
      clubs = []
      hubs = []
      node = 0
      for i in range(self.params['numclubs']):
         clubs.append([])
         for j in range(int(clubsizes[i])):
            clubs[i].append(node)
            node += 1
      
      for i in range(numhubs):
         hubs.append(node)
         node += 1
      
      print("CLUBS:"+str(clubs))
      print("HUBS:"+str(hubs))
      ####################################################


      ####################################################
      # Build adjacency matrix
      #
      self.ADJ = numpy.zeros([self.n, self.n])
      drivers = []
      # Clubs, green edges
         # For each club, place a random edges 0.75-1 between every pair
         # Revised TMC 7/7/15: Connections are fueld by a driver
         # So: Pick a random driver in the club
         # Give each other node in the club, relatively high magnitude edge
         # All tertiary edges should be less than the others with the driver
      for j in range(0, self.params['numdrivers']):
        club = clubs[j]
        driver = random.randint(min(club), max(club))
        drivers.append(driver)
        print("Driver: "+str(driver)+" (common friend)")
        for node1 in club:
            if (node1 != driver):
               self.ADJ[node1][driver] = random.random()*0.15 + 0.85
               self.ADJ[driver][node1] = self.ADJ[node1][driver]
      for j in range(self.params['numdrivers'], self.params['numclubs']):
        club = clubs[j]
        driver = random.randint(min(club), max(club))
        drivers.append(driver)
        print("Driver: "+str(driver)+" (common enemy)")
        for node1 in club:
            if (node1 != driver):
               self.ADJ[node1][driver] = random.random()*0.15 + -1
               self.ADJ[driver][node1] = self.ADJ[node1][driver]
      k = 0
      for club in clubs:
         for i in range(len(club)):
            for j in range(i+1, len(club)):
                   node1 = club[i]
                   node2 = club[j]
                   if (node1 not in drivers and node2 not in drivers):  
                     self.ADJ[node1][node2] = random.random()*(min(abs(self.ADJ[node1][drivers[k]]), abs(self.ADJ[node2][drivers[k]]))-0.75)+0.75
                     self.ADJ[node2][node1] = self.ADJ[node1][node2]
         k += 1

      # Rival clubs, red edges
      # We can just make the first however many clubs, rival clubs
      for i in range(self.params['numrivalclubs']):
         clubA = clubs[i]
         for j in range(i+1, numrivalclubs):
            clubB = clubs[j]
            for node1 in clubA:
               for node2 in clubB: 
                  self.ADJ[node1][node2] = random.random()*0.5 + -0.5
                  self.ADJ[node2][node1] = self.ADJ[node1][node2]


      # Hubs.  Choose one node from two random clubs and join to each hub
      # Random positive weight, 0.75-1
      for hub in hubs:
         randomclub1 = clubs[random.randint(0, self.params['numclubs']-1)]
         randomclub2 = clubs[random.randint(0, self.params['numclubs']-1)]
         while (randomclub2 == randomclub1):
            randomclub2 = clubs[random.randint(0, self.params['numclubs']-1)]
         randomnode1 = random.randint(min(randomclub1), max(randomclub1))
         randomnode2 = random.randint(min(randomclub2), max(randomclub2))
         print("Connecting "+str(hub)+" to "+str(randomnode1)+" and "+str(randomnode2))
         self.ADJ[hub][randomnode1] = random.random()*0.25 + 0.75
         self.ADJ[randomnode1][hub] = self.ADJ[hub][randomnode1]
         self.ADJ[hub][randomnode2] = random.random()*0.25 + 0.75
         self.ADJ[randomnode2][hub] = self.ADJ[hub][randomnode2]


      # Common Enemies.  For each, pick a random club and join
      # each node with random red edges.
      #for commonenemy in commonenemies:
      #   randomclub = clubs[random.randint(0, numclubs-1)]
      #   for node in randomclub:
      #      self.ADJ[node][commonenemy] = random.random()*0.25 + -1
      #      self.ADJ[commonenemy][node] = self.ADJ[node][commonenemy]


      # Noise.  Pick random nodes, and draw light green edges.
      # Note these must already have node edge between them
      noisyedges = int(round(self.params['pctnoise'] * self.n))
      i = 0
      while (i < noisyedges):
         randomnode1 = random.randint(0, n-1)
         randomnode2 = random.randint(0, n-1)
         if (randomnode1 != randomnode2 and self.ADJ[randomnode1][randomnode2] == 0):
            self.ADJ[randomnode1][randomnode2] = random.random()*0.5 
            self.ADJ[randomnode2][randomnode1] = self.ADJ[randomnode1][randomnode2]
         i += 1

   def output(self, filename):
      gmlfile = open(filename, 'w')
      gmlfile.write("graph [\n")
      for i in range(self.n):
         gmlfile.write("node [\n")
         gmlfile.write("id "+str(i)+"\n")
         gmlfile.write("label \"A"+str(i)+"\"\n")
         gmlfile.write("]\n")
      for i in range(self.n):
         for j in range(i+1, self.n):
          if (self.ADJ[i][j] != 0):
            gmlfile.write("edge [\n")
            gmlfile.write("source "+str(i)+"\n")
            gmlfile.write("target "+str(j)+"\n")
            gmlfile.write("weight "+str(self.ADJ[i][j])+"\n")
            gmlfile.write("]\n")
      gmlfile.write("]\n")






      




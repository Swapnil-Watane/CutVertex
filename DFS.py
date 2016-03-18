class CodeGraph:

	def __init__(self, gnm, numnode):
		self.graphname = gnm
		self.numnodes = numnode
		self.nodes = [None] * numnode

	# method in CodeGraph class starts with 'g'
	# set graph name
	def gsetname(self, gnm):
		self.graphname = gnm
	
	# get graph name
	def ggetname(self):
		return self.graphname

	# set graph number of nodes
	def gsetnumofnodes(self, nds):
		self.numnodes = nds

	# get graph number of nodes
	def ggetnumofnodes(self):
		return self.numnodes

	# set graph node
	def gsetnode(self, nd):
		n = Nodes(nd)
		self.nodes[nd-1] = n

	# get graph all nodes
	def ggetnodes(self):
		return self.nodes

	# get graph node
	def ggetnode(self, nd):
		return self.nodes[nd-1]
	
	# set node adjacent
	def gsetadjnodes(self, nd, adj):
		#import pdb; pdb.set_trace()
		self.nodes[nd-1].setadjnodes(adj)
	
	# get node adjacent
	def ggetadjnodes(self, nd):
		return self.nodes[nd-1].getadjnodes()

	# add adjacency for remaining nodes which only 
	#appeared as adjacent to some node
	def addremadjacent(self, remadj):
		if None in self.nodes:
			var = self.nodes.index(None) + 1
			Flag = True
		else:
			Flag = False

		if Flag:
			self.gsetnode(var)
			for adj in remadj:
				if str(var) in adj:
					for i in adj.split():
						if '-' in i:
							self.gsetadjnodes(var, -int(i))
							break
			self.addremadjacent(remadj)
	
	# fix if node a appears to be adjacent of b 
	# but b does not have a in its adjacency list.
	def correctadjacent(self):
		for i in self.nodes:
			mn = i.vernm
			for j in i.adjver:
				if mn not in self.nodes[j-1].adjver:
					self.gsetadjnodes(j, mn)


class Nodes:
	def __init__(self, nm):
		self.vernm = nm
		self.adjver = []
		self.parent = None

	# get node name
	def getnodenm(self):
		return self.vernm

	# set node adjacent
	def setadjnodes(self, adj):
		self.adjver.append(adj)

	# get node adjacent
	def getadjnodes(self):
		return self.adjver

	# set node parent
	def setparent(self, par):
		self.parent = par

	# get node parent
	def getparent(self):
		return self.parent


def main():

	# Read the input graph.
	
	fnm = raw_input("Please enter name of input file: ")
	print "\nYou entered:", fnm
	rd = open(fnm, 'r')
	data = ''
	rdgraph = []
	
	# This code is reading all data from first line as provided
	# in assignment programming question.
	
	while 1:
		line = rd.readline()
		#import pdb; pdb.set_trace()
		if not line:
			break
		else: 
			data = line
	rd.close()
	gfnm = ''
	tmp = 0    
	ct = 1		# counter
	nodes = 0	# number of vertices
	remainingadj = []
	val = ''
	flag = 0
	
	for detail in data.split():
		if ct == 1:
			gfnm = detail
			ct = ct + 1
		elif ct == 2:
			graph = CodeGraph(gfnm, int(detail)) 
			ct = ct + 1
		elif ct == 3:
			if int(detail) == 0:
				remainingadj.append(val)
				break
			if int(detail) < 0:
				if flag == 1:
					remainingadj.append(val)
					val = ''
	
				graph.gsetnode(-int(detail))
				# tmp is used to store u and connect all v to it.
				tmp = -int(detail)
				flag = 1
			else:
				graph.gsetadjnodes(tmp, int(detail))
				val = val + " " + str(-tmp) + " " + detail
	
	# correction method
	graph.addremadjacent(remainingadj)

	# correction method
	graph.correctadjacent()

	DFCount = 0
	DFNum = [0] * graph.ggetnumofnodes()
	LowPt = [None] * graph.ggetnumofnodes()
	stackedge = []
	cutverstack = []


	# set low point
	# val, val
	def slowpt(who, what):
		LowPt[who-1] = what

	# get low point
	# val
	def glowpt(who):
		return LowPt[who-1]

	# set DFNum
	# val, val
	def sdfnum(who, what):
		DFNum[who-1] = what

	# get DFNum
	# val
	def gdfnum(who):
		return DFNum[who-1]

	# set parent
	# obj, val
	def spar(who, what):
		who.setparent(what)

	# get parent
	# obj
	def gpar(who):
		return who.getparent()
	
	# print node and its adjacency	
	print "\n******* Node and its adjacency *******\n"
	for i in graph.ggetnodes():
		print "       ", i.vernm, "     ",i.adjver
	print "\n***************************************\n"
	
	# DFSearch method
	def dfsearch(u, DFCount):
		DFCount = DFCount + 1
		sdfnum(u.getnodenm(), DFCount)
		for i in u.getadjnodes():
			v = graph.ggetnode(int(i))
			if gdfnum(i) == 0:
				spar(v, u.getnodenm())
				edge = str(u.getnodenm())+"-" + str(i)
				stackedge.append(edge)
				slowpt(i, gdfnum(u.getnodenm()))
				dfsearch(v, DFCount)
				if glowpt(i) == gdfnum(u.getnodenm()):
					cutverstack.append(u.getnodenm())

					print "\n",cutverstack[len(cutverstack)-2], " is a cut vertex. Edges in a block are as below:\n"
					edge = str(u.getnodenm())+"-" + str(i)
					while 1:
						edg = stackedge.pop()
						print "     ", edg
						if edg == edge:
							break
				elif glowpt(i) < glowpt(u.getnodenm()):
					slowpt(u.getnodenm(), glowpt(i))
			elif i != gpar(u):
				if gdfnum(i) < gdfnum(u.getnodenm()):
					edge = str(u.getnodenm())+"-" + str(i)
					stackedge.append(edge)
					if gdfnum(i) < glowpt(u.getnodenm()):
						slowpt(u.getnodenm(), gdfnum(i))


	
	
	u = graph.ggetnode(4)
	slowpt(u.getnodenm(), 1)
	# call DFSearch with u
	dfsearch(u, DFCount)


if __name__ == '__main__':
	main()

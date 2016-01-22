from math import *
import json
from geopy.distance import vincenty
from collections import defaultdict
import heapq
from fibonacciheap import FibonacciHeap

class ServiceCenter(object):
    def __init__(self,name,latitude,longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.coordinate = (latitude,longitude)
        self.number = int(name[-1:])

#Read from json file
#Return list of ServiceCenter objects
def readData(src):
	result=[]
	with open(src) as inf:
		for line in inf:
			j = json.loads(line)
			result.append(ServiceCenter(**j))
	return result

#Return  distance between two ServiceCenter objects
def distance(src,dest):
	#Vicenty's formulae are used for their accuracy due to assuming
	#oblate spheroid Earth over great-circle distance method, 
	#which assumes a spherical Earth (Vicenty, 1975)

	#Coded to python from Inverse Problem of Wikipedia

	#We use WGS-84, which is the most widely used ellipsoid
	#major (km), minor(km), flattening
	a=6378.137
	b=6356.7523142
	f = 1 / 298.257223563
	#Difference in longitude
	L = radians(dest.longitude) - radians(src.longitude)
	#Reduced latitude
	U1 = atan((1-f)*tan(radians(src.latitude)))
	U2 = atan((1-f)*tan(radians(dest.latitude)))
	#Iterate until convergence or reach iteration limit
	lam = L
	lamP = pi*2
	#Iteration counter
	iter_num = 100
	#Begin iteration
	while abs(lam-lamP)>10**-12 and iter_num!=0:
            iter_num -= 1
            sin_lam, cos_lam = sin(lam), cos(lam)
            sin_sigma = sqrt((cos(U2) * sin_lam) ** 2 + (cos(U1) * sin(U2) -
            	sin(U1) * cos(U2) * cos_lam) ** 2)

            #Special cases
            #In case of same point
            if sin_sigma == 0:
                return 0 
            cos_sigma = (sin(U1) * sin(U2) + cos(U1) * cos(U2) * cos_lam)
            sigma = atan2(sin_sigma, cos_sigma)
            sin_alpha = (cos(U1) * cos(U2) * sin_lam / sin_sigma)
            cos_sq_alpha = 1 - sin_alpha ** 2
            #In case of equator
            if cos_sq_alpha != 0:
                cos2_sigma_m = cos_sigma - 2 * (sin(U1) * sin(U2) / cos_sq_alpha)
            else:
                cos2_sigma_m = 0

            C = f / 16 * cos_sq_alpha * (4 + f * (4 - 3 * cos_sq_alpha))
            lamP = lam
            lam = (L + (1 - C) * f * sin_alpha * (sigma + C * sin_sigma * 
            	(cos2_sigma_m + C * cos_sigma * (-1 + 2 * cos2_sigma_m ** 2))))
	#End of iteration
	u_sq = cos_sq_alpha * (a ** 2 - b ** 2) / b ** 2
	A = 1 + u_sq / 16384. * (4096 + u_sq * (-768 + u_sq * (320 - 175 * u_sq)))
	B = u_sq / 1024. * (256 + u_sq * (-128 + u_sq * (74 - 47 * u_sq)))
	delta_sigma = (B * sin_sigma * (cos2_sigma_m + B / 4. * (cos_sigma * 
		(-1 + 2 * cos2_sigma_m ** 2) - B / 6. * cos2_sigma_m * 
		(-3 + 4 * sin_sigma ** 2) * (-3 + 4 * cos2_sigma_m ** 2))))
	distance = b * A * (sigma - delta_sigma)
	return distance

def createGraph(centers):
	g = defaultdict(dict)
	for i in centers:
		for j in centers:
			d = distance(i,j)
			#Insert condition to remove distance >20 km
			if d<=20:
				g[i.name][j.name]=d
				#List all available distances
				#print i.name,"to",j.name,"is",d

	return g

#NOT USED!
#Fibonacci-heap-based Dijkstra's Algorithm to find the shortest path (Fredman and Tarjan, 1987)
def fibo_shortest(g,src):
	q = FibonacciHeap()
	dist = {}
	prev = {}

	#Set all node distances to infinity, source distance to 0
	for v in g.keys():
		dist[v] = float("inf")
		prev[v] = None
		dist[src]=0
		q.insert(dist[v], v)
	

	while not q.n==0:
		#Select the source node
		u = q.extract_min().data
		for v in g[u]:
			alt = dist[u] + g[u][v]
			if alt < dist[v]:
				dist[v] = alt
				prev[v] = u
				#The next line needs to implement a find operation,
				#which would affect run time according to Cook (2012)
				q.decrease_key(v,alt)
	return dist, prev

#Binary-heap-based Dijkstra's Algorithm to find the shortest path
#Makrai (2015) shows runtime to be inferior to Fibonacci heap
#but still superior once taken into account that we don't need
#a find operation (Cook, 2012)
def binary_shortest(g,src,dest):
	#Set up binary priority queue, distance and predecessor dicts
	q = []
	dist = {}
	prev = {}
	#Set all node distances to infinity, source distance to 0
	for v in g.keys():
		dist[v] = float("inf")
		dist[src]=0
		heapq.heappush(q, (dist[v], v))

	while len(q)>0:
		#Select the source node
		u = heapq.heappop(q)
		#Trace the neighbors
		for v in g[u[1]]:
			#Calculate alternate distance
			alt = dist[u[1]] + g[u[1]][v]
			#Apply alternate distance if shorter
			if alt < dist[v]:
				dist[v] = alt
				heapq.heappush(q, (dist[v], v))
				prev[v] = u[1]
	#Return distance and predecessor nodes before destinations
	return (dist, prev)

#Reverse iteration to find the individual shortest path
def reverse_path(g, src, dest):
	#Get distance and precessor input
	dist, prev = binary_shortest(g,src,dest)
	#Set up path list
	path=[]
	#Keep appending predecessors until source is reached
	while True:
		path.append(dest)
		if dest==src: break
		dest = prev[dest]
	#Reverse the list so it's src -> dest
	path.reverse()
	#Return ([path],Distance in km)
	return path, dist[path[-1]]

if __name__ == "__main__":
	centers = readData('servicecenter.json')
	g = createGraph(centers)
	#Print all shortest routes and distances
	for i in g.keys():
		for j in g.keys():
			print reverse_path(g,i,j)
	

#References
#Cook, Mary Rose. "The Fibonacci Heap Ruins My Life." Weblog post. Mary Rose Cook. N.p., 7 Aug. 2012. Web. 22 Jan. 2016.
#Fredman, Michael L., and Robert Endre Tarjan. "Fibonacci Heaps and Their Uses in Improved Network Optimization Algorithms." Journal of the ACM JACM J. ACM 34.3 (1987): 596-615.
#Makrai, Gabor. "Experimenting with Dijkstra's Algorithm." Weblog post. Gabor Makrai's Blog. N.p., 11 Feb. 2015. Web. 22 Jan. 2016.
#"Vincenty's Formulae." Wikipedia. Wikimedia Foundation, n.d. Web. 22 Jan. 2016.
#Vincenty, T. "Direct And Inverse Solutions Of Geodesics On The Ellipsoid With Application Of Nested Equations." Survey Review 23.176 (1975): 88-93.


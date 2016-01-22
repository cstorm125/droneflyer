# droneflyer
Answer to CodeStar question

![Service Centers](https://cloud.githubusercontent.com/assets/15519308/12521225/fabaaad0-c17b-11e5-95ba-cf43942b9155.png)
## answer.py
To run
```
python answer.py servicecenter.json
```
Return all tuples of shortest routes and distance among service centers
Example:
```
([u'Service Center 1'], 0)
([u'Service Center 1', u'Service Center 2'], 14.084315289418088)
([u'Service Center 1', u'Service Center 3'], 17.02688647416232)
([u'Service Center 1', u'Service Center 3', u'Service Center 4'], 34.00991571179068)
([u'Service Center 1', u'Service Center 3', u'Service Center 4', u'Service Center 5'], 48.31237019535092)
([u'Service Center 1', u'Service Center 2', u'Service Center 6'], 31.84711690306566)
([u'Service Center 2', u'Service Center 1'], 14.084315289418038)
```
### Vincenty's Formulae
Vicenty's formulae are used for their accuracy due to assuming an oblate spheroid Earth over great-circle distance method, which assumes a spherical Earth (Vicenty, 1975). We use the WGS-84--which is said to be the most widely used and accurate--for the calculation. The code was derived by the author from [Vicenty's Inverse Problem on Wikipedia](https://en.wikipedia.org/wiki/Vincenty%27s_formulae#Inverse_problem)
### Djikstra's Algorithm
In order to find the shortest paths among service centers, we use the greedy, breadth-first Djikstra's algorithm with binary heap.

## servicecenter.json
Assume that the location of the service centers are stored in a JSON file.

## fibonacciheap.py
Implementation of [Fibonacci Heap](https://github.com/ksang) by Ksang
I initially included the Fibonacci Heap into the implementation due to Fredman and Tarjan (1987). However, I ran into the same problem as Cook (2012) for the fact that this particular implementation of the Fibonacci Heap needs a *find* operation for it to work with Dijsktra's algorithm, which will defeat the purpose of a smaller big O. Therefore, In the current implementation, a binary heap is used.


## References
Cook, Mary Rose. "The Fibonacci Heap Ruins My Life." Weblog post. Mary Rose Cook. N.p., 7 Aug. 2012. Web. 22 Jan. 2016.

Fredman, Michael L., and Robert Endre Tarjan. "Fibonacci Heaps and Their Uses in Improved Network Optimization Algorithms." Journal of the ACM JACM J. ACM 34.3 (1987): 596-615.

Makrai, Gabor. "Experimenting with Dijkstra's Algorithm." Weblog post. Gabor Makrai's Blog. N.p., 11 Feb. 2015. Web. 22 Jan. 2016.

"Vincenty's Formulae." Wikipedia. Wikimedia Foundation, n.d. Web. 22 Jan. 2016.

Vincenty, T. "Direct And Inverse Solutions Of Geodesics On The Ellipsoid With Application Of Nested Equations." Survey Review 23.176 (1975): 88-93.


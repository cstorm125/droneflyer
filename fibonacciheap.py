#Source: https://github.com/ksang
NEGATIVE_INFINITY = -10e10000

class FibonacciHeap:

    class Node:

        __slots__ = ['left','right','parent','child','key','data','degree','mark']

        def __init__(self):
            self.left = None
            self.right = None
            self.parent = None
            self.child = []

            self.key = None
            self.data = None

            self.degree = 0
            self.mark = False

    def __init__(self):
        self.min = None
        self.n = 0

    def minimun(self):
        return (self.min.key, self.min.data)

    def remove_from_list(self, x):
        x.left.right = x.right
        x.right.left = x.left
        x.left = x.right = x

    def cut(self, x, y):
        # Cut x from child list of y and add it to root list
        if x.right is x:
            y.child.remove(x)
        else:
            y.child.remove(x)
            y.child.append(x.right)
            self.remove_from_list(x)
        y.degree -= 1
        x.parent = None
        x.mark = False
        # Cut operations doesn't need to update min, because child
        # is larger than parent which is already in root list
        self.concatenate(self.min, x)

    def cascading_cut(self, y):
        # Recursively cut y from it's parent depends on the mark status
        z = y.parent
        if z is not None:
            if y.mark == False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    def heap_link(self, y, x):
        # Remove y from root list and link it as a child of x
        self.remove_from_list(y)
        y.parent = x
        x.child.append(y)

        x.degree += 1
        y.mark = False

    def concatenate(self, y, x):
        # Concatenate two circular double link into one.
        # It is important to have circular link rather than normal link.
        # otherwise can't achieve this in O(1) time.
        # 'x' and 'y' are two nodes of two circular double links.
        # It's caller's duty to make sure they are not in the same link already,
        # otherwise this will break the existing link.
        if x is None:
            return y
        elif y is None:
            return x

        saved_x_right = x.right
        x.right = y.right
        x.right.left = x
        y.right = saved_x_right
        y.right.left = y
                             
        if x.key < y.key:
            return x
        else:
            return y

    def consolidate(self):
        # Make all root list nodes have different degree
        # to keep root list size below O(log(n)).
        # Here we take advantage of python's hash map dictionary
        # to make a degree array A
        A = {}
        root_list = []
        start = curr = self.min
        root_list.append(curr)
        curr = curr.right
        while curr is not start:
            root_list.append(curr)
            curr = curr.right

        # Traverse root list to check node degree, if there are nodes with
        # same degree, make the one has larger key be the child of other.   
        for x in root_list:
            d = x.degree
            while A.get(d) is not None:
                y = A[d]
                if x.key > y.key:
                    tmp = x
                    x = y
                    y = tmp
                self.heap_link(y, x)
                A[d] = None
                d += 1
            A[d] = x
            x = x.right
        # Rebuild root list by traversing "A"
        self.min = None
        for a in A.values():
            if a is not None:
                self.remove_from_list(a)
                self.min = self.concatenate(a, self.min)

    def merge(self, aheap):
        # Merge another Fibonacci heap into this one.
        self.min = self.concatenate(self.min, aheap.min)
        self.n = self.n + aheap.n

    def insert(self, k, d):
        x = self.Node()
        x.key = k
        x.data = d
        # Make itself a singleton circular
        x.left = x.right = x
        self._insert(x)

    def _insert(self, x):
        self.min = self.concatenate(x, self.min)
        self.n += 1

    def extract_min(self):
        # Remove min from root circular link list
        minimun = self.min

        if minimun is not None:
            # Clear min's child's parent flag and add them to root list
            for child in minimun.child:
                curr = child
                while True:
                    curr.parent = None
                    curr = curr.right
                    if curr is child:
                        break        
                self.min = self.concatenate(self.min, child)
            # Remove min from root list
            saved_right = minimun.right
            self.remove_from_list(minimun)
            if saved_right is minimun:
                self.min = None
            else:
                self.min = saved_right
                self.consolidate()
            self.n -= 1
            
        return minimun

    def _decrease_key(self, x, k):
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self.cut(x, y)
            self.cascading_cut(y)
        if x.key < self.min.key:
            self.min = x

    def decrease_key(self, x, k):
        # Decrease node x's key value by k, then modify heap
        if k > x.key:
            raise ValueError('New key is greater than current key.')
            return
        self._decrease_key(x, k)

    def delete(self, x):
        self._decrease_key(x, NEGATIVE_INFINITY)
        self.extract_min()
import random

class HamiltonianCycle:
    def __init__(self, m, n):
        # m x n grid
        self.m = m
        self.n = n
        self.cycle = [[-1 for i in range(n)] for j in range(m)]

        self.createCycle()
    
    def createCycle(self):
        # generate a random maze of half the size, and it can be expanded to be a Hamiltonian Cycle
        m = self.m//2
        n = self.n//2
        # set edges between every adjacent pair of nodes in grid with half dimensions to have random weights
        self.edges = []
        for i in range(m-1):
            for j in range(n-1):
                self.edges.append([i*n+j, (i+1)*n+j, random.random()])
                self.edges.append([i*n+j, i*n+j+1, random.random()])
        
        for i in range(m-1):
            self.edges.append([(i+1)*n-1, (i+2)*n-1, random.random()])
        
        for j in range(n-1):
            self.edges.append([(m-1)*n + j, (m-1)*n + j + 1, random.random()])
        
        # idea is to find the MST of the graph to create the random maze
        # I use'd Kruskal's Union Find algorithm to find MST
        self.edges.sort(key=lambda a : a[2])

        self.link = [i for i in range(m*n)]
        self.size = [1 for i in range(m*n)]
        self.mst = [set([]) for i in range(m*n)]

        for edge in self.edges:
            if not self.same(edge[0], edge[1]):
                self.unite(edge[0], edge[1])
                self.mst[edge[0]].add(edge[1])
                self.mst[edge[1]].add(edge[0])
        # some logic to make a Hamiltonian Cycle in the original grid based on the MST
        self.cycle_edges = [set([]) for i in range(self.m*self.n)]
        for i in range(m):
            for j in range(n):
                if (i-1)*n+j in self.mst[i*n+j]:
                    self.cycle_edges[i*2*self.n+j*2].add(i*2*self.n+j*2 - self.n)
                    self.cycle_edges[i*2*self.n+j*2 + 1].add(i*2*self.n+j*2 - self.n+1)
                else:
                    self.cycle_edges[i*2*self.n+j*2].add(i*2*self.n+j*2 + 1)
                    self.cycle_edges[i*2*self.n+j*2 + 1].add(i*2*self.n+j*2)
                if (i+1)*n+j in self.mst[i*n+j]:
                    self.cycle_edges[i*2*self.n+j*2 + self.n].add(i*2*self.n+j*2 + 2*self.n)
                    self.cycle_edges[i*2*self.n+j*2 + self.n+1].add(i*2*self.n+j*2 + 2*self.n+1)
                else:
                    self.cycle_edges[i*2*self.n+j*2 + self.n].add(i*2*self.n+j*2 + self.n+1)
                    self.cycle_edges[i*2*self.n+j*2 + self.n+1].add(i*2*self.n+j*2 + self.n)
                if i*n+j+1 in self.mst[i*n+j]:
                    self.cycle_edges[i*2*self.n+j*2 + 1].add(i*2*self.n+j*2 + 2)
                    self.cycle_edges[i*2*self.n+j*2 + self.n+1].add(i*2*self.n+j*2 + self.n+2)
                else:
                    self.cycle_edges[i*2*self.n+j*2 + 1].add(i*2*self.n+j*2 + self.n+1)
                    self.cycle_edges[i*2*self.n+j*2 + self.n+1].add(i*2*self.n+j*2 + 1)
                if i*n+j-1 in self.mst[i*n+j]:
                    self.cycle_edges[i*2*self.n+j*2].add(i*2*self.n+j*2 - 1)
                    self.cycle_edges[i*2*self.n+j*2 + self.n].add(i*2*self.n+j*2 + self.n-1)
                else:
                    self.cycle_edges[i*2*self.n+j*2].add(i*2*self.n+j*2 + self.n)
                    self.cycle_edges[i*2*self.n+j*2 + self.n].add(i*2*self.n+j*2)
        # traverse the cycle and mark the path order in self.cycle
        # tried to dfs, but stack size got too big with certain grid sizes
        curr = 0
        cnt = 0
        while cnt < self.m*self.n:
            self.cycle[curr//self.n][curr%self.n] = cnt
            cnt += 1
            for next in self.cycle_edges[curr]:
                if self.cycle[next//self.n][next%self.n] == -1:
                    curr = next
                    break
                else:
                    continue

    # Union Find helper functions
    def find(self, x):
        while(x != self.link[x]):
            x = self.link[x]
        return x
    
    def same(self, a, b):
        return self.find(a) == self.find(b)
    
    def unite(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if(self.size[a] < self.size[b]):
            temp = a
            a = b
            b = temp
        self.size[a] += self.size[b]
        self.link[b] = a
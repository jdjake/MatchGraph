from graph import Graph
import random
from copy import copy

class ColorGraph:
    def __init__(self, V = None, E = []):
        self.d_colors = V or {} 
        self.g = Graph(set(V.keys()) if V else set(), E)
    
    def add_vertex(self, v, color):
        self.d_colors[v] = color
        self.g.add_vertex(v)

    # get's color of node v
    def get_color(self, v):
        return self.d_colors[v]

    def _get_random_color(self):
        COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (76, 0, 153)]

        random.seed()
        return random.choice(COLORS)

    def _swap_colors(self, v1, v2):
        temp = self.get_color(v1)
        self.d_colors[v1] = self.get_color(v2)
        self.d_colors[v2] = temp

    def _can_swap(self, v1, v2):
        ocolor1 = self.get_color(v1)
        ocolor2 = self.get_color(v2)

        for n in self.g.neighbours(v1):
            if ocolor2 == self.get_color(n):
                return True

        for n in self.g.neighbours(v2):
            if ocolor1 == self.get_color(n):
                return True

        return False

    # first check's if it can swap
    # then swaps and deletes accordingly
    # returns a list of nodes deleted
    def swap_vertices(self, v1, v2):        
        if not self._can_swap(v1, v2):
            return []
        else:
            self._swap_colors(v1,v2)
            tup = self.delete_vertex(v1, self._get_random_color())
            if self.g.is_vertex(v2):
                tup2 = self.delete_vertex(v2, self._get_random_color())
                for n in self.g.neighbours(v2):
                    self.g.add_edge((v1, n))
                self.g.remove_vertex(v2)
                return tup[1] + tup2[1] + [v2]
            return tup[1]

    def delete_vertex(self, v, new_color):
        Q = [v] 
        # The Queue: needs v to prevent checking later

        Qi = 1 
        # The current Queue index (skips v)

        to_add = [] 
        # vertices that will be attatched to v

        delete = []
        # vertices to be deleted by main.py

        ocolor = self.get_color(v) 
        # node v's color (for comparison)

        # adding neighbours to queue for checking 
        neigh = self.g.neighbours(v)
        for n in neigh:
            Q.append(v)

        # as long as the queue is not finished
        while Qi < len(Q):
            # current node being checked
            current = Q[Qi]

            # if the current node matches node v
            if self.get_color(current) == ocolor:
                neigh = self.g.neighbours(current)
                if current != v:
                    delete.append(current)
                    self.g.remove_vertex(current)
                    self.d_colors.pop(current)
                for n in neigh:
                    if self.get_color(n) == ocolor and n not in Q:
                        Q.append(n)
                    elif self.get_color(n) != ocolor:
                        to_add.append(n)

            # else will connect the node to node v at the end
            # if color does not match node v
            else: 
                to_add.append(n)

            # go to next index in Queue
            Qi += 1

        # adds the edges required
        for v2 in to_add:
            self.g.add_edge((v,v2))

        # finally, changes node v's color
        self.d_colors[v] = new_color

        return (v, delete)

    def delete_get_colors(self):
        return self.d_colors

    def vertices(self):
        return self.g.vertices()

    def edges(self):
        return self.g.edges()

    def remove_vertex(self, v):
        self.g.remove_vertex(v)

    def neighbours(self, vertex):
        return self.g.neighbours(vertex)

    def partition_graph(self):
	partition = []

        vertex_stack = self.vertices()
        while vertex_stack:
            current_partition = set(vertex_stack.pop())
            partition_to_add = copy(current_partition)
            while current_partition:
                v = current_partition.pop()
                vertex_stack.discard(v)
                
                for neighbour in self.neighbours(v):
                    if self.get_color(neighbour) == self.get_color(v) and neighbour not in partition_to_add:
                        current_partition.add(neighbour)
                        partition_to_add.add(neighbour)

            partition.append(partition_to_add)

        return partition

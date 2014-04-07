from graph import Graph
import random

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

    def delete_vertex(self, v, new_color):
        Q = [v] 
        # The Queue: needs v to prevent checking later

        Qi = 1 
        # The current Queue index (skips v)

        to_add = [] 
        # vertices that will be attatched to v

        ocolor = self.get_color(v) 
        # node v's color (for comparison)

        # the player's score
        score = 1

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
                    self.g.remove_vertex(current)
                    self.d_colors.pop(current)
                    score += 1
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

        return score

    def delete_get_colors(self):
        return self.d_colors

    def vertices(self):
        return self.g.vertices()

    def edges(self):
        return self.g.edges()

    def remove_vertex(self, v):
        self.g.remove_vertex(v)

import random

from graph import Graph
from copy import copy
from itertools import product

class ColorGraph():
    """
    A graph with added functionality to add colour to each of the nodes, along
    with added functionality for implementing the matching game.
    """

    def __init__(self, vertex_colors = [], edges = []):
        """
        Given a list of vertex, color tuples, and a list of edges, this
        function creates a ColorGraph.

        >>> a = ColorGraph([(1,"RED"),(2,"BLUE")],[(1,2)])
        >>> a.graph.adjacency_dict
        {1: {2}, 2: set()}
        >>> a.vertex_colors
        {1: 'RED', 2: 'BLUE'}
        """

        self.vertex_colors = {vertex:color for vertex,color in vertex_colors}

        vertices = [vertex for vertex, color in vertex_colors]
        self.graph = Graph(vertices, edges)
        self.score = 0

    def add_vertex(self, vertex, color):
        """
        Given a vertex and its colour, adds it to a colour graph.

        >>> a = ColorGraph()
        >>> a.add_vertex(1, "RED")
        >>> a.vertex_colors
        {1: 'RED'}
        >>> a.add_vertex(2,"BLUE")
        >>> a.vertex_colors
        {1: 'RED', 2: 'BLUE'}
        """

        self.vertex_colors[vertex] = color
        self.graph.add_vertex(vertex)

    def get_color(self, vertex):
        """
        Returns the colour corresponding to the given vertex in the graph.

        >>> a = ColorGraph([(1,"RED"), (2,"BLUE")], [])
        >>> a.get_color(1)
        'RED'
        >>> a.get_color(2)
        'BLUE'
        """

        if not self.graph.is_vertex(vertex):
            raise ValueError("Vertex {} not in graph".format(vertex))

        return self.vertex_colors[vertex]

    def get_score(self):
        return self.score

    def change_score(self, change):
        self.score += change

    def get_random_color(self):
        """
        Chooses a random color for a vertex from a specific selection.
        """

        COLORS = ["RED", "GREEN", "BLUE", "PURPLE"]

        random.seed()
        return random.choice(COLORS)

    def swap_colors(self, vertex_1, vertex_2):
        """
        Swaps the colours of two vertices in the graph.

        >>> a = ColorGraph([(1,"RED"),(2,"BLUE")])
        >>> a.swap_colors(1,2)
        >>> a.get_color(1)
        'BLUE'
        >>> a.get_color(2)
        'RED'
        """

        self.vertex_colors[vertex_1], self.vertex_colors[vertex_2]      \
          = self.get_color(vertex_2), self.get_color(vertex_1)

    def find_partition(self, start_node):
        """
        Given a node, this function finds all other nodes connected in a
        component like fashion with the same color.
        """

        current_partition = set([start_node])
        total_partition = copy(current_partition)

        partition_color = self.get_color(start_node)

        # Now we do a depth first search on the vertices, adding vertices
        # to our partition that share a common edge and are the same color.
        while current_partition:
            vertex = current_partition.pop()

            same_color = lambda x: self.get_color(x) == partition_color
            maybe_neighbors = filter(same_color, self.graph.neighbours(vertex))

            for neighbor in maybe_neighbors:
                if neighbor not in total_partition:
                    current_partition.add(neighbor)
                    total_partition.add(neighbor)

        return total_partition

    def partition_graph(self):
        """
        Partitions graph into sets of nodes connected together which have
        the same colour.

        >>> c_colors = [(1, "RED"),  (2, "RED"), (3, "RED"), (4, "BLUE"), \
                        (5, "BLUE"), (6, "RED"), (7, "RED")]
        >>> c_edges = [(1,2), (2,3), (1,4), (3,5), (5,6), (4,7)]
        >>> c = ColorGraph(c_colors, c_edges)
        >>> c.partition_graph()
        [{1, 2, 3}, {4}, {5}, {6}, {7}]
        """

        partition = []

        unvisited_vertices = self.graph.vertices()

        # We work through vertices one by one, forming partitions as we go.
        while unvisited_vertices:
            new_partition_start = unvisited_vertices.pop()
            new_partition = self.find_partition(new_partition_start)

            for vertex in new_partition:
                unvisited_vertices.discard(vertex)

            partition.append(new_partition)

        return partition

    def can_swap(self, vertex_1, vertex_2):
        """
        Checks if two vertices can be swapped, given the limitations of the
        game (vertices swapped must make a group of 3).

        >>> c_colors = [(1, "RED"),  (2, "RED"), (3, "RED"), (4, "BLUE"), \
                        (5, "BLUE"), (6, "RED"), (7, "RED")]
        >>> c_edges = [(1,2), (2,3), (1,4), (3,5), (5,6), (4,7)]
        >>> c = ColorGraph(c_colors, c_edges)
        >>> c.can_swap(5, 6)
        True
        >>> c.can_swap(4, 5)
        False
        """

        # We cannot swap two nodes if they don't have an edge between them.
        if self.graph.is_edge(vertex_1, vertex_2):
            self.swap_colors(vertex_1, vertex_2)
            partitions = self.partition_graph()
            self.swap_colors(vertex_1, vertex_2)

            # If we have a group of 3, then we can definitely swap the two.
            if [x for x in partitions if len(x) >= 3]:
                return True

        return False

    def remove_vertex(self, vertex):
        """
        Removes a vertex from the graph.

        >>> a = ColorGraph([(1,"RED"),(2,"BLUE")],[(1,2)])
        >>> a.remove_vertex(1)
        >>> a.graph.adjacency_dict
        {2: set()}
        >>> a.vertex_colors
        {2: 'BLUE'}
        """

        self.vertex_colors.pop(vertex)
        self.graph.remove_vertex(vertex)

    def remove_partitions(self, partitions):
        """
        Removes all partitions specified, adding edges between all the
        nodes originally connected to the partition. Returns a list of all
        nodes deleted.
        """

        deleted = []

        for partition in partitions:
            self.change_score(len(partition))

            neighbors = [y for x in partition for y in self.graph.neighbour(x)]
            new_neighbors = [x for x in neighbors if x not in partition]

            possible_connect = [x for x in product(new_neighbors,new_neighbors)]
            to_connect = [(x,y) for x,y in possible_connect if x != y]

            for vertex_1, vertex_2 in to_connect:
                self.graph.add_edge(vertex_1, vertex_2)

            for element in partition:
                self.remove_vertex(element)
                deleted.append(element)

        return deleted

    def swap_vertices(self, vertex_1, vertex_2):
        """
        Checks if two vertices can be swapped, and if they can, swaps the two
        nodes and deletes all other nodes that would be deleted from the swap.
        The function determines a list of vertices deleted and the score scored.
        """

        deleted = []

        if not self.can_swap(vertex_1, vertex_2):
            return deleted

        self.swap_colors(vertex_1, vertex_2)
        deletable = [x for x in self.partition_graph() if len(x) > 2]

        while deleteable:
            deleted += self.remove_partitions(deleteable)

            # We now see if we've caused a chain reaction, in which case
            # we start the deletion process all over again.
            deleteable = [x for x in self.partition_graph() if len(x) > 2]

        return deleted

    def get_two_partitions(self):
        """
        Returns all color partitions in the graph that have 2 or more elements.
        """

        large_partitions = [x for x in self.partition_graph() if len(x) > 1]
        return {x for partition in large_partitions for x in partition}
from graph import Graph
import random
from copy import copy

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

            # We begin by popping an arbitrary vertex to start a new component.
            current_partition = set([new_partition_start])
            partition_to_add = copy(current_partition)

            partition_color = self.get_color(new_partition_start)

            # Now we do a depth first search on the vertices, adding vertices
            # to our partition that share a common edge and are the same color.
            while current_partition:
                vertex = current_partition.pop()

                # If we've scanned a vertex, we no longer need to look at it to
                # find more partitions (it's already in the one we're forming)
                unvisited_vertices.discard(vertex)

                for neighbour in self.graph.neighbours(vertex):
                    if (self.get_color(neighbour) == partition_color
                      and neighbour not in partition_to_add):
                        current_partition.add(neighbour)
                        partition_to_add.add(neighbour)

            partition.append(partition_to_add)

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

    def swap_vertices(self, vertex_1, vertex_2):
        """
        Checks if two vertices can be swapped, and if they can, swaps the two
        nodes and deletes all other nodes that would be deleted from the swap.
        The function determines a list of vertices deleted and the score scored.
        """

        score = 0
        deleted = []

        if self.can_swap(vertex_1, vertex_2):
            self.swap_colors(vertex_1, vertex_2)
            deletable = [x for x in self.partition_graph() if len(x) > 2]

            while deleteable:
                # For each partition, we delete all edges in the partition, then
                # connect together all edges that were connected to the partition
                for partition in deletable:
                    score += len(partition)

                    neighbours = [neighbour for x in partition
                      for neighbour in self.graph.neighbours(x)
                      if neighbour not in partition]

                    for vertex_from in neighbours:
                        to_add_edge = [x for x in neighbours if x != vertex_from]
                        for neighbour_to in to_add_edge:
                            self.graph.add_edge(vertex_from, vertex_to)

                    for element in partition:
                        self.remove_vertex(element)
                        deleted.append(element)

                # We see if there is now a chain reaction occuring, in which
                # case we start the deletion process all over again.
                deleteable = [x for x in self.partition_graph() if len(x) > 2]

        return score**2, deleted

    def get_two_partitions(self):
        """
        Returns all color partitions in the graph that have 2 or more elements.
        """

        large_partitions = [x for x in self.partition_graph() if len(x) > 1]
        return {x for partition in large_partitions for x in partition}
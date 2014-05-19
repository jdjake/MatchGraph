# Thanks to this great article on 'Force Directed Graphs' for giving a simple method
# to distribute the graph
#      http://cs.brown.edu/~rt/gdhandbook/chapters/force-directed.pdf

import pygame

from random import randint
from math import log, acos, sin, cos
from sys import exit
from time import sleep
from colorgraph import ColorGraph
from vector import Vector
from collections import defaultdict

def in_range(vector_1, vector_1_radius, vector_2, vector_2_radius):
    """
    Given two vectors, which we can see as circles/spheres/hypermegaspheres
    if given a radius, this function tests whether the two vectors with
    these radii overlap given a position and size.

    >>> a = Vector(0, 0)
    >>> in_range(a, 0.1, a, 0.1)
    True
    >>> b = Vector(10,0)
    >>> in_range(a, 10, b, 10)
    True
    >>> in_range(a, 4, b, 4)
    False
    """

    space_between_vectors = (vector_1 - vector_2).norm()
    combined_radii = vector_1_radius + vector_2_radius

    return space_between_vectors < combined_radii

def random_coord(vertex):
    """
    Returns a random coordinate within 10
    screen lengths from the centre of the map.
    """

    x_coordinate = randint(-10*screen_width, 10*screen_width)
    y_coordinate = randint(-10*screen_height, 10*screen_height)

    return Vector(x_coordinate, y_coordinate)

def get_new_coordinate(vertex):
    """
    Returns a new coordinate vector, randomly placed on the map
    and tested to ensure it does not overlap with another vertex.
    """

    new_coordinate = random_coord(vertex)

    for other_vertex in vertex_coordinates:
        if in_range(new_coordinate, vertex_sizes[vertex],
                vertex_coordinates[other_vertex], vertex_sizes[other_vertex]):
            return get_new_coordinate(vertex)

    return new_coordinate

def draw_graph(graph):
    """ Using pygame, draws the map on the screen """

    not_in_coordinates = lambda x: x not in vertex_coordinates
    not_coordinates = filter(not_in_coordinates, graph.graph.vertices())
    for vertex in not_coordinates:
        vertex_coordinates[vertex] = get_new_coordinate(vertex)

    for edge_1, edge_2 in graph.graph.edges():
        vector_1  = vertex_coordinates[edge_1]*magnification + offset
        coord_1 = tuple(int(x) for x in vector_1)

        vector_2 = vertex_coordinates[edge_2]*magnification + offset
        coord_2 = tuple(int(x) for x in vector_2)

        thickness = int(50*magnification)

        pygame.draw.line(screen, COLOURS["WHITE"], coord_1, coord_2, thickness)

    for vertex in graph.graph.vertices():
        vertex_color = COLOURS[graph.get_color(vertex)]

        magnified = [int(x*magnification) for x in vertex_coordinates[vertex]]
        center = Vector(*magnified) + offset
        radius = int(vertex_sizes[vertex]*magnification)

        pygame.draw.circle(screen, vertex_color, center, radius)

def update_screen_image(graph):
    screen.fill(COLOURS["BLACK"])
    draw_graph(graph)

def gravitate_nodes(vertices, cycles):
    for i in range(cycles):
        for vertex in vertex_coordinates:
            total_force = Vector(0, 0)

            # Edge Spring Force
            for x,y in (x for x in graph.graph.edges() if x[0] == vertex):
                distance = vertex_coordinates[y] - vertex_coordinates[x]

                x_negative = -1 if distance[0] < 0 else 1
                y_negative = -1 if distance[1] < 0 else 1

                force = Vector(vertex_sizes[y]/10*x_negative*log(abs(distance[0])) if distance[0] > 0 else 1,
                        vertex_sizes[y]/10*y_negative*log(abs(distance[1])) if distance[1] > 0 else 1)

                total_force += force

            # Repulsive Force
            for other_vertex in (x for x in vertex_coordinates if x != vertex):
                distance = vertex_coordinates[other_vertex] - vertex_coordinates[vertex]

                x_negative = 1 if distance[0] < 0 else -1
                y_negative = 1 if distance[1] < 0 else -1

                force = Vector(x_negative/(distance[0]/300000)**2/vertex_sizes[other_vertex] if distance[0] else 1,
                        y_negative/(distance[1]/300000)**2/vertex_sizes[vertex] if distance[1] else 1)

                total_force += force

            # Attaction to Center
            distance = vertex_coordinates[vertex] - screen_center

            x_negative = 1 if distance[0] < 0 else -1
            y_negative = 1 if distance[1] < 0 else -1

            force = Vector(x_negative*75*log(abs(distance[0])) if distance[0] > 0 else 1,
                    y_negative*75*log(abs(distance[1])) if distance[1] > 0 else 1)

            total_force += force

            vertex_coordinates[vertex] += total_force*10/vertex_sizes[vertex]

        update_screen_image(graph)

def selected_vertex(mouse_position):
    for vertex in vertex_coordinates:
        if in_range(mouse_position, 5, vertex_coordinates[vertex], vertex_sizes[vertex]):
            return vertex

    return None

def print_selected_vertex(x):
    pygame.draw.circle(screen, COLOURS["WHITE"],
            Vector(*(int(x*magnification) for x in vertex_coordinates[x])) + offset, int((vertex_sizes[x]+20)*magnification))
    pygame.draw.circle(screen, COLOURS[graph.get_color(x)],
            Vector(*(int(x*magnification) for x in vertex_coordinates[x])) + offset, int(vertex_sizes[x]*magnification))

def remove_display_vertex(graph, vertex):
    vertex_sizes.pop(vertex)
    vertex_coordinates.pop(vertex)





pygame.init()
myfont = pygame.font.SysFont("monospace", 15)

# Dictionary containing the RGB values for Colours
COLOURS = {"RED":(255, 0, 0), "GREEN":(0, 255, 0),
        "BLUE":(0, 0, 255), "YELLOW":(255, 255, 0),
        "PURPLE":(76, 0, 153), "BLACK":(0, 0, 0),
        "WHITE":(255,255,255)}

screen_width = 1200
screen_height = 1000
screen_center = Vector(screen_width//2, screen_height//2)

screen = pygame.display.set_mode((screen_width, screen_height))

# Test graph
"""vertices = {1:"RED", 2:"RED", 3:"BLUE", 4:"GREEN", 5:"PURPLE", 6:"BLUE", 7:"PURPLE",
    8:"BLUE", 9:"GREEN", 10:"RED"}
edges = [(1,2),(2,1),(3,4),(4,3),(4,2),(2,4),(3,5),(5,3),(1,6),(6,1), (7,8), (8,7), (7,9), (9,7), (6,9), (9,6),
	(3,10),(10,3), (4,10), (10,4), (3,6), (6,3), (8,9), (9,8)]"""

#complete graph
"""edges = [(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),
        (2,1),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),
        (3,1),(3,2),(3,4),(3,5),(3,6),(3,7),(3,8),(3,9),
        (4,1),(4,2),(4,3),(4,5),(4,6),(4,7),(4,8),(4,9),
        (5,1),(5,2),(5,3),(5,4),(5,6),(5,7),(5,8),(5,9),
        (6,1),(6,2),(6,3),(6,4),(6,5),(6,7),(6,8),(6,9),
        (7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,8),(7,9),
        (8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,9),
        (9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8)]"""

vertices = [(1,"RED"), (2,"BLUE"), (3,"RED"), (4,"BLUE"), (5,"BLUE"), (6,"RED")]
edges = [(1,2), (2,3), (3,4), (4,5), (5,6)]

vertices = [(1,"RED"),     (2,"RED"),    (3,"RED"),    (4,"RED"),
            (5,"RED"),     (6,"RED"),    (7,"RED"),    (8,"BLUE"),
            (9,"BLUE"),    (10,"BLUE"),  (11,"BLUE"),  (12,"BLUE"),
            (13,"GREEN"),  (14,"GREEN"), (15,"GREEN"), (16,"GREEN"),
            (17,"GREEN"),  (18,"GREEN"), (19,"PURPLE"), (20,"PURPLE"), 
            (21,"PURPLE"), (22,"PURPLE")]
edges = [( 1,  2), ( 1,  8), ( 1, 14), ( 1, 19), ( 2,  1), ( 3,  8), ( 3,  9),
         ( 3, 14), ( 4, 19), ( 5, 16), ( 6, 12), ( 7, 13), ( 7, 18), ( 7, 22),
         (10, 19), (10, 16), (11, 16), (12, 17), (12, 18), (12, 21), (15, 19),
         (16, 20), ( 4, 13), ( 4, 20), ( 5, 21), ( 4, 22), ( 6, 22), ( 9, 11)]

graph = ColorGraph(vertices, edges)

# Set of vectors representing where vertices are on the screen
vertex_coordinates = {}

# Pixel radius of vertex
vertex_sizes = defaultdict(lambda: randint(100,150))

first_mouse_clicked = True
first_selected = None

score = 0
offset = Vector(0, 0)
magnification = 1

to_highlight = set()

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # (0, 0) top-left
            mouse_position = Vector(*tuple(x/magnification for x in Vector(*(pygame.mouse.get_pos())) - offset))
            print("Clicked Mouse at {0}".format(mouse_position))

            x = selected_vertex(mouse_position)

            if first_mouse_clicked:
                if x:
                    first_selected = x
                    first_mouse_clicked = False

                    print(vertex_sizes[x])
                    print("Selected Vertex {}".format(x))

            else:
                # If no element was selected
                if not x:
                    first_mouse_clicked = True
                    first_selected = None
                    print("Deselected Vertex")
                else:
                    # Do stuff to swap vertices
                    first_mouse_clicked = True

                    added_score, to_delete = graph.swap_vertices(first_selected, x)
                    score += added_score

                    if to_delete:                        
                        vertex_coordinates[first_selected], vertex_coordinates[x] = vertex_coordinates[x], vertex_coordinates[first_selected]

                        for deletion in to_delete:
                            remove_display_vertex(graph, deletion)

                        print("Swapping Vertex {} with Vertex {}".format(first_selected, x))
                    
                first_selected = None        

                update_screen_image(graph)
                label = myfont.render("Score: {}".format(score), 1, (255, 255, 0))
                screen.blit(label, (0, 0))

        if event.type == pygame.KEYDOWN:
            keys_pressed = {pygame.key.name(index) for index,key in
                    enumerate(pygame.key.get_pressed()) if key == 1}
            print("Clicked {0} key".format(keys_pressed))

            if 'space' in keys_pressed:
                offset = Vector(0, 0)

            if 'left' in keys_pressed:
                offset += Vector(-50, 0)

            if 'right' in keys_pressed:
                offset += Vector(50, 0)

            if 'down' in keys_pressed:
                offset += Vector(0, 50)

            if 'up' in keys_pressed:
                offset += Vector(0, -50)

            if 'z' in keys_pressed:
                # Zoom in
                magnification *= 2

            if 'x' in keys_pressed:
                # Zoom out
                magnification *= 0.5

            if 'r' in keys_pressed:
                vertex_coordinates.clear()
                vertex_sizes.clear()

            if 'c' in keys_pressed:
                to_highlight = graph.highlight_twos()

            if 'v' in keys_pressed:
                to_highlight = set()

            if 'escape' in keys_pressed:
                print("Finished")
                exit()

            #update_screen_image(graph)

    gravitate_nodes(graph, 1)

    if first_selected:
        print_selected_vertex(first_selected)

    label = myfont.render("Score: {}".format(score), 12, (255, 255, 0))
    screen.blit(label, (0, 0))

    pygame.display.flip()
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

def random_coord(vertex):
    x_coordinate = randint(0, screen_width)
    y_coordinate = randint(0, screen_height)

    return Vector(x_coordinate, y_coordinate)

def in_range(vertex_1, vertex_1_size, vertex_2, vertex_2_size):
    """
    Tests whether two vertices overlap, based on their position and size
    """

    return (vertex_1 - vertex_2).norm() < vertex_1_size + vertex_2_size

def get_new_coordinate(vertex):
    """
    Returns a new coordinate vector, randomly placed on the map and tested to ensure
    it does not overlap with another vertex.
    """

    new_coordinate = random_coord(vertex)

    for other_vertex in vertex_coordinates:
        if in_range(new_coordinate, vertex_sizes[vertex],
                vertex_coordinates[other_vertex], vertex_sizes[other_vertex]):
            return get_new_coordinate(vertex)

    return new_coordinate

def draw_graph(graph):
    for vertex in graph.vertices():
        if vertex not in vertex_coordinates:
            vertex_coordinates[vertex] = get_new_coordinate(vertex)

    for edge_1, edge_2 in graph.edges():
        pygame.draw.line(screen, COLOURS["WHITE"],
                vertex_coordinates[edge_1] + offset,
                vertex_coordinates[edge_2] + offset, 10)

    for vertex in graph.vertices():
        vertex_color = COLOURS[graph.get_color(vertex)]

        pygame.draw.circle(screen, vertex_color,
                Vector(*(int(x) for x in vertex_coordinates[vertex])) + offset, vertex_sizes[vertex])


def update_screen_image(graph):
    screen.fill(COLOURS["BLACK"])
    draw_graph(graph)

def gravitate_nodes(vertices, cycles):
    for i in range(cycles):
        for vertex in vertex_coordinates:
            total_force = Vector(0, 0)

            # Edge Spring Force
            for x,y in (x for x in graph.edges() if x[0] == vertex):
                distance = vertex_coordinates[y] - vertex_coordinates[x]

                x_negative = -1 if distance[0] < 0 else 1
                y_negative = -1 if distance[1] < 0 else 1

                force = Vector(vertex_sizes[y]/80*x_negative*log(abs(distance[0])) if distance[0] > 0 else 1,
                        vertex_sizes[y]/80*y_negative*log(abs(distance[1])) if distance[1] > 0 else 1)

                total_force += force

            # Repulsive Force
            for other_vertex in (x for x in vertex_coordinates if x != vertex):
                distance = vertex_coordinates[other_vertex] - vertex_coordinates[vertex]

                x_negative = 1 if distance[0] < 0 else -1
                y_negative = 1 if distance[1] < 0 else -1

                force = Vector(x_negative/(distance[0]/7500)**2/vertex_sizes[other_vertex] if distance[0] else 1,
                        y_negative/(distance[1]/7500)**2/vertex_sizes[vertex] if distance[1] else 1)

                total_force += force

            # Attaction to Center
            distance = vertex_coordinates[vertex] - screen_center

            x_negative = 1 if distance[0] < 0 else -1
            y_negative = 1 if distance[1] < 0 else -1

            force = Vector(x_negative*30*log(abs(distance[0])) if distance[0] > 0 else 1,
                    y_negative*30*log(abs(distance[1])) if distance[1] > 0 else 1)

            total_force += force

            vertex_coordinates[vertex] += total_force*10/vertex_sizes[vertex]

        update_screen_image(graph)

def selected_vertex(mouse_position):
    for vertex in vertex_coordinates:
        if in_range(mouse_position, 0, vertex_coordinates[vertex], vertex_sizes[vertex]):
            return vertex

    return None

def print_selected_vertex(x):
    pygame.draw.circle(screen, COLOURS["WHITE"],
            Vector(*(int(x) for x in vertex_coordinates[x])) + offset, vertex_sizes[x] + 5)
    pygame.draw.circle(screen, COLOURS[graph.get_color(x)],
            Vector(*(int(x) for x in vertex_coordinates[x])) + offset, vertex_sizes[x])

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
vertices = {1:"RED", 2:"RED", 3:"BLUE", 4:"GREEN", 5:"PURPLE", 6:"BLUE", 7:"PURPLE",
    8:"BLUE", 9:"GREEN"}
edges = [(1,2),(2,1),(3,4),(4,3),(4,2),(2,4),(3,5),(5,3),(1,6),(6,1), (7,8), (8,7), (7,9), (9,7), (6,9), (9,6)]

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

graph = ColorGraph(vertices, edges)

# Set of vectors representing where vertices are on the screen
vertex_coordinates = {}

# Pixel radius of vertex
vertex_sizes = defaultdict(lambda: randint(50,90))

first_mouse_clicked = True
first_selected = None

score = 0
offset = Vector(0, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # (0, 0) top-left
            mouse_position = Vector(*pygame.mouse.get_pos()) - offset
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

                    vertex_coordinates[first_selected], vertex_coordinates[x] = vertex_coordinates[x], vertex_coordinates[first_selected]

                    to_delete = graph.swap_vertices(first_selected, x)

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
                pass

            if 'x' in keys_pressed:
                # Zoom out
                pass

            if 'r' in keys_pressed:
                vertex_coordinates.clear()
                vertex_sizes.clear()

            if 'escape' in keys_pressed:
                print("Finished")
                exit()

            #update_screen_image(graph)

    gravitate_nodes(graph, 10)

    if first_selected:
        print_selected_vertex(first_selected)

    label = myfont.render("Score: {}".format(score), 12, (255, 255, 0))
    screen.blit(label, (0, 0))

    pygame.display.flip()

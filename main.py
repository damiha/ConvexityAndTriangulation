import pygame
import numpy as np
import math
from compute_geometry import *
from draw_geometry import *
from globals import *

# Initialize Pygame
pygame.init()

# Set up the display

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Convexity And Triangulation")

# Main game loop
running = True
clock = pygame.time.Clock()

polygon1 = [
    np.array([100, 100]),
    np.array([400, 100]),
    np.array([400, 400]),
    np.array([100, 400])
]

polygon2 = [
    np.array([100, 100]),
    np.array([200, 300]),
    np.array([400, 400]),
    np.array([100, 400])
]

polygon3 = [
    np.array([425, 695]),
    np.array([675, 370]),
    np.array([465, 400]),
    np.array([370, 175]),
    np.array([320, 260]),
    np.array([145, 165]),
    np.array([192, 292]),
    np.array([75, 440]),
    np.array([212, 406]),
    np.array([186, 616]),
    np.array([338, 524])
]

def translate(polygon, offset):
    return [p + offset for p in polygon]

mouse_pressed = False

polygon2 = translate(polygon2, np.array([300, 300]))

#triangles1 = ear_clipping_triangulation(polygon1)
triangles2 = ear_clipping_triangulation(polygon2)
triangles3 = ear_clipping_triangulation(polygon3)

polygon4 = [
    np.array([100, 400]),
    np.array([300, 100]),
    np.array([500, 100]),
    np.array([700, 400]),
    np.array([500, 700]),
    np.array([400, 300]),
    np.array([300, 700])
]


convex_polygon_3 = convex_polygon_from_points(polygon3)
convex_polygon_4 = convex_polygon_from_points(polygon4)

triangles4 = ear_clipping_triangulation(polygon4)
#print(convex_polygon_3)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False

    # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    #print(f"Mouse position: ({mouse_x}, {mouse_y})")

    # Fill the screen with white
    screen.fill(WHITE)

    #draw_points_and_outline(polygon1)#
    draw_points_and_outline(screen, polygon3, color=RED)
    draw_points_and_outline(screen, convex_polygon_3, color=BLUE, draw_text=False)
    #draw_points_and_outline(polygon4)
    #draw_points_and_outline(screen, convex_polygon_4, color=RED)
    #draw_triangulation(screen, triangles4, color=GREEN)

    #draw_triangulation(triangles1)
    #draw_triangulation(triangles3)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
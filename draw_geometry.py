import pygame
from globals import *

def draw_points_and_outline(screen, polygon, color=BLACK, draw_points=False, draw_text=True):
    font = pygame.font.Font(None, 24)  # You can adjust the font size here

    for i, p in enumerate(polygon):
        next_p = polygon[(i + 1) % len(polygon)]

        if color is not None:
            pygame.draw.line(screen, color, p, next_p, 2)

        # Draw the point
        if draw_points:
            pygame.draw.circle(screen, RED, p, 4, 0)

        # Render the index number
        text = font.render(str(i), True, BLUE)  # Blue text

        # Position the text slightly offset from the point
        text_pos = (p[0] + 10, p[1] - 10)

        # Draw the text
        if draw_text:
            screen.blit(text, text_pos)

def draw_triangulation(screen, triangles, color=BLACK):

    for triangle in triangles:

        pygame.draw.line(screen, color, triangle[0], triangle[1])
        pygame.draw.line(screen, color, triangle[1], triangle[2])
        pygame.draw.line(screen, color, triangle[2], triangle[0])
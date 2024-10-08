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


def translate(polygon, offset):
    return [p + offset for p in polygon]

mouse_pressed = False
shift_pressed = False
c_key_pressed = False
show_help = False

space_key_pressed = False
start_selection_box = None
end_selection_box = None

point_radius = 6
# more tolerance when selecting
selection_radius = 12
indices_selected_points = []
selection_is_ordered = None

points = []
polygons = []
polygons_convex = []
triangulations = []

max_time_between_double_click = 0.2
time_between_double_click = -1

dt = 0

def draw_points(points):

    for i, point in enumerate(points):
        pygame.draw.circle(screen, color=BLACK, center=point, radius=point_radius)

        if i in indices_selected_points:
            pygame.draw.circle(screen, color=BLACK, center=point, radius=point_radius + 4, width=1)

def get_index_of_selected(points, mouse_pos):

    for i, point in enumerate(points):

        distance = np.linalg.norm(point - mouse_pos)

        if distance <= selection_radius:
            return i

    return None

def point_in_polygon(point, polygon):

    for polygon_point in polygon:
        if np.all(polygon_point == point):
            return True
    return False


def draw_controls(screen, show_help):
    font = pygame.font.Font(None, 24)

    if show_help:
        controls = [
            "create point = double left click",
            "select point = left click",
            "select multiple points = left click + [Shift]",
            "select region = drag mouse + [Space]",
            "create polygon = [P] (after selection)",
            "triangulate polygon = [T] (after selection)",
            "create convex hull = [H] (after selection)",
            "check convexity = [C]"
        ]
    else:
        controls = ["[Esc] to show controls"]

    margin = 10
    line_height = 30
    screen_width = screen.get_width()

    for i, text in enumerate(controls):
        surface = font.render(text, True, (0, 0, 0))  # Black text
        rect = surface.get_rect()
        rect.topright = (screen_width - margin, margin + i * line_height)
        screen.blit(surface, rect)

def get_top_left_bottom_right(start_selection_box, end_selection_box):
    top_left = np.array(
        [min(start_selection_box[0], end_selection_box[0]), min(start_selection_box[1], end_selection_box[1])])
    bottom_right = np.array(
        [max(start_selection_box[0], end_selection_box[0]), max(start_selection_box[1], end_selection_box[1])])

    return top_left, bottom_right

def draw_selection_box(start_selection_box, end_selection_box):

    top_left, bottom_right = get_top_left_bottom_right(start_selection_box, end_selection_box)
    pygame.draw.rect(screen, BLACK, (top_left, bottom_right - top_left), width=2)

while running:

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True

            if not space_key_pressed:
                index_selected = get_index_of_selected(points, np.array([mouse_x, mouse_y]))

                if index_selected is not None:
                    indices_selected_points = (indices_selected_points + [index_selected]) if shift_pressed else [index_selected]
                    selection_is_ordered = True

                else:

                    indices_selected_points = []
                    selection_is_ordered = None

                    # click into empty space, double click is possible
                    if time_between_double_click == -1:
                        time_between_double_click = 0

                    elif 0 <= time_between_double_click <= max_time_between_double_click:

                        points.append(np.array([mouse_x, mouse_y]))
                        time_between_double_click = -1

            else:

                start_selection_box = np.array([mouse_x, mouse_y])

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift_pressed = True

            if event.key == pygame.K_h:

                if len(indices_selected_points) >= 3:
                    convex_polygon = convex_polygon_from_points([points[i] for i in indices_selected_points])
                    polygons_convex.append(True)
                    polygons.append(convex_polygon)

            if event.key == pygame.K_p:

                if len(indices_selected_points) >= 3 and selection_is_ordered:
                    polygon_to_append = [points[i] for i in indices_selected_points]
                    polygons.append(polygon_to_append)

                    polygons_convex.append(is_convex(polygon_to_append))

            if event.key == pygame.K_c:
                c_key_pressed = True

            if event.key == pygame.K_SPACE:
                space_key_pressed = True

            if event.key == pygame.K_ESCAPE:
                show_help = not show_help

            if event.key == pygame.K_t:

                # only closed polygons can be triangulated
                if len(indices_selected_points) > 0:

                    selected_point = points[indices_selected_points[0]]

                    polygons_selected = [polygon for polygon in polygons if point_in_polygon(selected_point, polygon)]

                    for selected_polygons in polygons_selected:
                        triangulations.append(ear_clipping_triangulation(selected_polygons))

            # Check for key release events
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift_pressed = False

            if event.key == pygame.K_c:
                c_key_pressed = False

            if event.key == pygame.K_SPACE:
                space_key_pressed = False

                selection_is_ordered = False

                top_left, bottom_right = get_top_left_bottom_right(start_selection_box, end_selection_box)

                for i, p in enumerate(points):

                    if np.all(p >= top_left) and np.all(p <= bottom_right):
                        indices_selected_points.append(i)

                start_selection_box = None
                end_selection_box = None



    # set and reset double click counter
    if time_between_double_click >= 0:
        time_between_double_click += dt

    if time_between_double_click > max_time_between_double_click:
        time_between_double_click = -1

    # Get the current mouse position

    #print(f"Mouse position: ({mouse_x}, {mouse_y})")

    # Fill the screen with white
    screen.fill(WHITE)

    for i, triangulation in enumerate(triangulations):
        color = BLACK if not c_key_pressed else (GREEN if polygons_convex[i] else RED)
        draw_triangulation(screen, triangulation, color)

    for i, polygon in enumerate(polygons):
        color = BLACK if not c_key_pressed else (GREEN if polygons_convex[i] else RED)
        draw_points_and_outline(screen, polygon, color)

    draw_points(points)

    draw_controls(screen, show_help)

    if space_key_pressed and start_selection_box is not None:
        end_selection_box = np.array([mouse_x, mouse_y])
        draw_selection_box(start_selection_box, end_selection_box)


    # Update the display
    pygame.display.flip()

    # Cap the frame rate (but can be below)
    dt = clock.tick(60) / 1000

# Quit Pygame
pygame.quit()
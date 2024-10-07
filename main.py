import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Convexity And Triangulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Main game loop
running = True
clock = pygame.time.Clock()

polygon1 = [
    np.array([100, 100]),
    np.array([400, 100]),
    np.array([400, 400]),
    np.array([100, 400])
]
# need to be counterclockwise
polygon1 = list(reversed(polygon1))

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

# need to be counterclockwise
polygon2 = list(reversed(polygon2))

def translate(polygon, offset):
    return [p + offset for p in polygon]

def draw_points_and_outline(polygon):

    for i, p in enumerate(polygon):

        next_p = polygon[(i + 1) % len(polygon)]

        pygame.draw.line(screen, BLACK, p, next_p, 2)
        pygame.draw.circle(screen, (255, 0, 0), p, 4, 0)

def to_homogeneous(p):
    return np.array([p[0], p[1], 1.], dtype=float)

def inside_triangle(A, B, C, P):
    # can be described by a linear system
    # l1 * A + l2 * B + l3 * C = P (2 equations in 2D)
    # l1 + l2 + l3 = 1 (one equation)
    # check that l1, l2, l3 >= 0

    M = np.array([
        [A[0], B[0], C[0]],
        [A[1], B[1], C[1]],
        [1., 1., 1.]
    ])

    R = np.array([P[0], P[1], 1.]).reshape(3, 1)

    try:
        coords = np.matmul(np.linalg.inv(M), R)
        return True  if coords[0] >= 0 and coords[1] >= 0 and coords[2] >= 0 else False

    except:
        return False

def triangle_orientation(p1, p2, p3):

    m = np.array([
        to_homogeneous(p1),
        to_homogeneous(p2),
        to_homogeneous(p3)
    ])

    return +1 if np.linalg.det(m) >= 0 else -1

def is_convex(polygon):

    assert len(polygon) >= 3, "a polygon needs at least three vertices"

    # a polygon is convex iff all triangles are left turns / right turns

    orientation_first_three = triangle_orientation(polygon[0], polygon[1], polygon[2])

    n = len(polygon)

    for i in range(1, n):

        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        p3 = polygon[(i + 2) % n]

        orientation = triangle_orientation(p1, p2, p3)

        if orientation != orientation_first_three:
            return False

    return True

# naive algorithm to triangulate a simple polygon
# returns a list of list of points = list of triangles
# assume oriented counterclockwise
def ear_clipping_triangulation(polygon):

    n = len(polygon)

    assert n >= 3, "a polygon needs at least three vertices"

    if n == 3:
        return [polygon]

    # find an ear
    for i in range(n):

        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        p3 = polygon[(i + 2) % n]

        is_convex_angle = triangle_orientation(p1, p2, p3) < 0

        print(f"{p1}, {p2}, {p3} = {is_convex_angle}")

        if not is_convex_angle:
            continue

        all_other_outside = True

        for j in range(n - 3):

            # + 3 to start at first point after p3
            other_p = polygon[(i + 3 + j) % n]

            print(f"{other_p=}")

            if inside_triangle(p1, p2, p3, other_p):
                all_other_outside = False
                break

        print(f"{all_other_outside=}")

        if all_other_outside:

            # found ear
            ear = [p1, p2, p3]

            print(f"Found ear: {ear}")

            # exclude tip of the ear
            clipped_polygon = [p for k, p in enumerate(polygon) if k != (i + 1) % n]

            return [ear] + ear_clipping_triangulation(clipped_polygon)

    raise Exception("Should not be reached. Every simple polygon can be triangulated")

def draw_triangulation(triangles):

    for triangle in triangles:

        pygame.draw.line(screen, BLACK, triangle[0], triangle[1])
        pygame.draw.line(screen, BLACK, triangle[1], triangle[2])
        pygame.draw.line(screen, BLACK, triangle[2], triangle[0])

mouse_pressed = False

polygon2 = translate(polygon2, np.array([300, 300]))

#triangles1 = ear_clipping_triangulation(polygon1)
triangles2 = ear_clipping_triangulation(polygon2)
triangles3 = ear_clipping_triangulation(polygon3)

print(triangles2)

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
    draw_points_and_outline(polygon3)

    #draw_triangulation(triangles1)
    draw_triangulation(triangles3)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
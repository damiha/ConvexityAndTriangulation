from lib2to3.fixes.fix_import import traverse_imports

import numpy as np

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

def convex_polygon_from_points(points):

    n = len(points)

    assert n >= 3, "a polygon needs at least 3 points"

    # result is a convex polygon in counterclockwise orientation

    convex_polygon = []

    # points as tuples, easier for python
    pt = [(p[0], p[1]) for p in points]

    # start with the right most point
    p0 = sorted(pt, key=lambda p: -p[0])[0]

    convex_polygon.append(p0)

    last_p = p0
    found_loop = False

    while not found_loop:

        curr_p = None

        for p in pt:

            if p == last_p:
                continue

            if curr_p is None:
                curr_p = p
                continue

            # is point right of the line, pick as new curr_p
            # triangle orientation
            a = np.array([last_p[0], last_p[1]])
            b = np.array([curr_p[0], curr_p[1]])
            c = np.array([p[0], p[1]])

            if triangle_orientation(a, b, c) > 0:
                # clockwise oriented triangle
                # p to the right of the line
                curr_p = p

        if curr_p in convex_polygon:
            found_loop = True
        else:
            convex_polygon.append(curr_p)
            last_p = curr_p

    return convex_polygon

# naive algorithm to triangulate a simple polygon
# returns a list of list of points = list of triangles
# assume oriented counterclockwise
def _ear_clipping_triangulation(polygon):

    n = len(polygon)

    if n == 3:
        return [polygon]

    # find an ear
    for i in range(n):

        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        p3 = polygon[(i + 2) % n]

        is_convex_angle = triangle_orientation(p1, p2, p3) < 0

        #print(f"{p1}, {p2}, {p3} = {is_convex_angle}")

        if not is_convex_angle:
            continue

        all_other_outside = True

        for j in range(n - 3):

            # + 3 to start at first point after p3
            other_p = polygon[(i + 3 + j) % n]

            #print(f"{other_p=}")

            if inside_triangle(p1, p2, p3, other_p):
                all_other_outside = False
                break

        #print(f"{all_other_outside=}")

        if all_other_outside:

            # found ear
            ear = [p1, p2, p3]

            #print(f"Found ear: {ear}")

            # exclude tip of the ear
            clipped_polygon = [p for k, p in enumerate(polygon) if k != (i + 1) % n]

            return [ear] + _ear_clipping_triangulation(clipped_polygon)

    raise Exception("Should not be reached. Every simple polygon can be triangulated")

def ear_clipping_triangulation(polygon):

    assert len(polygon) >= 3, "a polygon needs at least three vertices"

    triangles = None

    try:
        triangles = _ear_clipping_triangulation(polygon)
    except:
        triangles = _ear_clipping_triangulation(list(reversed(polygon)))

    return triangles
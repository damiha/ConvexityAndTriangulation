
### Convexity And Triangulation

I wanted to learn (1) how to rasterize arbitrary (non-convex) simple polygons
and (2) how to convert a set of points into a convex polygon.

Part (1) is relatively straight forward. A simple polygon (no self intersection)
is given by an ordered list of points. We assume the polygon is closed (the last point is connected
to the first point). We split it into a set of triangles. This is
called triangulation, and we use the **ear clipping algorithm** for that. Filling out triangles
is easy: For every pixel with (x, y) coordinates, we check whether it is inside
the triangle (that involves finding the point's **barycentric coordinates** which boils down
to solving a linear system). If the point (x, y) is inside, we color it, otherwise, we don't.

Triangulation can also be used for testing whether two non-convex polygons intersect.
We just split the non-convex polygons into triangles and then test whether some
triangle of polygon A intersects some triangle of polygon B. We can also
merge adjacent triangles if the resulting shape remains convex. This way, we split
the non-convex polygon into multiple convex polygons (they don't have to be triangles).
Then, we could use **the separating axis theorem (SAT)** for the intersection test.

Part (2) is also not difficult. Given a set of points, calculating
the **convex hull** is done using the **gift wrapping algorithm**. The result
is a list of vertices that define the convex polygon.

Checking whether a polygon is convex can be done by looping over all points. For a point at index i,
pick the neighboring points at indices i - 1 and i + 1 and check whether the triangle
defined by the three points is **positively / negatively oriented**. If all such triangles
are positively oriented or all triangles are negatively oriented, the polygon
is convex. The orientation of a triangle can be found by calculating the determinant
of a 3x3 matrix. Its columns are the **homogeneous coordinates** of the three points.

### Demo

![Video](./gifs/triangulation_convexity.gif)


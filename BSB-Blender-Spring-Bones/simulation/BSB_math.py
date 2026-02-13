import math

from mathutils import Vector


def lerp_vec(vec_a, vec_b, t):
    return vec_a * t + vec_b * (1 - t)


def dot_product(vector_a: Vector, vector_b: Vector) -> float:
    return (vector_a.x * vector_b.x) + (vector_a.y * vector_b.y) + (vector_a.z * vector_b.z)


def project_point_onto_line(a, b, p):
    # project the point plane_point onto the line a,b
    ap = p - a
    ab = b - a

    fac_a = (p - a).dot(b - a)
    fac_b = (p - b).dot(b - a)

    result = a + ap.dot(ab) / ab.dot(ab) * ab

    if fac_a < 0:
        result = a
    if fac_b > 0:
        result = b

    return result


def project_point_onto_plane(point: Vector, plane_point: Vector,
                             plane_normal: Vector) -> Vector:
    """
    :param point: point source
    :type point: mathutils.Vector

    :param plane_point: point belonging to the plane
    :type plane_point: mathutils.Vector

    :param plane_normal: normal of the plane
    :type plane_normal: mathutils.Vector

    :return: projected point
    :rtype: mathutils.Vector
    """

    plane_normal = plane_normal.normalized()
    return point - ((point - plane_point).dot(plane_normal)) * plane_normal


def subregion(e, c, f):
    s = 0.0
    if e >= 0.0:
        t = 0.0
        distance_squared = f
    else:
        if -e >= c:
            t = 1.0
            distance_squared = c + 2.0 * e + f
        else:
            t = -e / c
            distance_squared = e * t + f

    return s, t


def project_point_onto_tri(point, tri: list[Vector]) -> Vector:
    """
    :param point:
    :param tri: tri vertex coordinates

    :type tri: list[list[float]]
    :return: projected point, point point_tri_a_distance
    """
    tri_a = tri[0]
    tri_b = tri[1]
    tri_c = tri[2]

    # return the point_tri_a_distance and the projected surface point
    # between a point and a triangle in 3D
    # original code: https://gist.github.com/joshuashaffer/
    # Author: Gwolyn Fischer

    edge_ab: Vector = tri_b - tri_a
    edge_ac = tri_c - tri_a

    point_tri_a_distance = tri_a - point

    edge_ab_len_sqrd: float = edge_ab.length_squared
    b = dot_product(edge_ab, edge_ac)
    c = dot_product(edge_ac, edge_ac)
    d = dot_product(edge_ab, point_tri_a_distance)
    e = dot_product(edge_ac, point_tri_a_distance)
    f = point_tri_a_distance.length_squared

    det = edge_ab_len_sqrd * c - b * b
    s = b * e - c * d
    t = b * d - edge_ab_len_sqrd * e

    # Terible tree of conditionals to determine in which region of the diagram
    # shown above the projection of the point into the triangle-plane lies.
    if (s + t) <= det:
        if s < 0.0:
            if t < 0.0:
                # region4
                if d < 0:
                    t = 0.0
                    if -d >= edge_ab_len_sqrd:
                        s = 1.0
                        distance_squared = edge_ab_len_sqrd + 2.0 * d + f
                    else:
                        s = -d / edge_ab_len_sqrd
                        distance_squared = d * s + f
                else:
                    subregion(e, c, f)
                    # of region 4
            else:
                # region 3
                subregion(e, c, f)
                # of region 3
        else:
            if t < 0:
                # region 5
                t = 0
                if d >= 0:
                    s = 0
                    distance_squared = f
                else:
                    if -d >= edge_ab_len_sqrd:
                        s = 1
                        distance_squared = edge_ab_len_sqrd + 2.0 * d + f  # GF 20101013 fixed typo d*s ->2*d
                    else:
                        s = -d / edge_ab_len_sqrd
                        distance_squared = d * s + f
            else:
                # region 0
                invDet = 1.0 / det
                s = s * invDet
                t = t * invDet
                distance_squared = s * (edge_ab_len_sqrd * s + b * t + 2.0 * d) + \
                                   t * (b * s + c * t + 2.0 * e) + f
    else:
        if s < 0.0:
            # region 2
            tmp0 = b + d
            tmp1 = c + e
            if tmp1 > tmp0:  # minimum on edge s+t=1
                numer = tmp1 - tmp0
                denom = edge_ab_len_sqrd - 2.0 * b + c
                if numer >= denom:
                    s = 1.0
                    t = 0.0
                    distance_squared = edge_ab_len_sqrd + 2.0 * d + f  # GF 20101014 fixed typo 2*b -> 2*d
                else:
                    s = numer / denom
                    t = 1 - s
                    distance_squared = s * (edge_ab_len_sqrd * s + b * t + 2 * d) + \
                                       t * (b * s + c * t + 2 * e) + f

            else:  # minimum on edge s=0
                s = 0.0
                if tmp1 <= 0.0:
                    t = 1
                    distance_squared = c + 2.0 * e + f
                else:
                    if e >= 0.0:
                        t = 0.0
                        distance_squared = f
                    else:
                        t = -e / c
                        distance_squared = e * t + f
                        # of region 2
        else:
            if t < 0.0:
                # region6
                tmp0 = b + e
                tmp1 = edge_ab_len_sqrd + d
                if tmp1 > tmp0:
                    numer = tmp1 - tmp0
                    denom = edge_ab_len_sqrd - 2.0 * b + c
                    if numer >= denom:
                        t = 1.0
                        s = 0
                        distance_squared = c + 2.0 * e + f
                    else:
                        t = numer / denom
                        s = 1 - t
                        distance_squared = s * \
                                           (edge_ab_len_sqrd * s + b * t + 2.0 * d) + t * \
                                           (b * s + c * t + 2.0 * e) + f

                else:
                    t = 0.0
                    if tmp1 <= 0.0:
                        s = 1
                        distance_squared = edge_ab_len_sqrd + 2.0 * d + f
                    else:
                        if d >= 0.0:
                            s = 0.0
                            distance_squared = f
                        else:
                            s = -d / edge_ab_len_sqrd
                            distance_squared = d * s + f
            else:
                # region 1
                numer = c + e - b - d
                if numer <= 0:
                    s = 0.0
                    t = 1.0
                    distance_squared = c + 2.0 * e + f
                else:
                    denom = edge_ab_len_sqrd - 2.0 * b + c
                    if numer >= denom:
                        s = 1.0
                        t = 0.0
                        distance_squared = edge_ab_len_sqrd + 2.0 * d + f
                    else:
                        s = numer / denom
                        t = 1 - s
                        distance_squared = s * \
                                           (edge_ab_len_sqrd * s + b * t + 2.0 * d) + t * \
                                           (b * s + c * t + 2.0 * e) + f

    # account for numerical round-off error
    if distance_squared < 0:
        distance_squared = 0

    dist = math.sqrt(distance_squared)

    PP0 = tri_a + s * edge_ab + t * edge_ac
    return dist, PP0

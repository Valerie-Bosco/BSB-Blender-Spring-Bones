from math import sqrt

import bpy
import mathutils
import numpy

from .BSB_Properties import (BSB_PG_ObjectProperties,
                             BSB_PG_PoseBoneProperties, BSB_PG_SpringBone)


def BSB_SpringBoneSimulationStep(context: bpy.types.Context):
    scene: bpy.types.Scene = context.scene
    depsgraph = context.evaluated_depsgraph_get()

    for spring_bone in scene.bsb_spring_bones:
        spring_bone: BSB_PG_SpringBone

        if spring_bone.bone_collider:
            continue

        armature = spring_bone.armature
        pose_bone: bpy.types.PoseBone = armature.pose.bones[spring_bone.name]
        pose_bone_properties: BSB_PG_PoseBoneProperties = pose_bone.bsb_pose_bone_properties

        if pose_bone_properties.global_influence == 0.0:
            continue

        empty_tail = bpy.data.objects.get(spring_bone.name + '_spring_tail')
        empty_head = bpy.data.objects.get(spring_bone.name + '_spring')

        if empty_tail == None or empty_head == None:
            return

        emp_tail_loc, rot, scale = empty_tail.matrix_world.decompose()

        axis_locked = pose_bone_properties.spring_axis_lock
        base_pos_dir = mathutils.Vector(
            (0, 0, -pose_bone_properties.spring_gravity))

        base_pos_dir += (emp_tail_loc - empty_head.location)

        if (spring_bone.b_is_bone_colliding):
            for bone_collider in scene.bsb_spring_bones:
                if bone_collider.bone_collider == False:
                    continue

                pose_bone_collider: BSB_PG_SpringBone = armature.pose.bones[bone_collider.name]
                # pose_bone_collider_radius = pose_bone_collider.collider_radius
                pose_bone_center = (pose_bone.tail + pose_bone.head) * 0.5
                p = project_point_onto_line(
                    pose_bone_collider.head, pose_bone_collider.tail, pose_bone_center)
                col_dir = (pose_bone_center - p)
                dist = col_dir.magnitude

                # if dist < pose_bone_collider_radius:
                #     push_vec = col_dir.normalized() * (pose_bone_collider_radius - dist) * \
                #         pose_bone_collider.sb_collider_force
                #     if axis_locked != "NONE" and axis_locked != None:
                #         if axis_locked == "+Y":
                #             direction_check = pose_bone.y_axis.normalized().dot(push_vec)
                #             if direction_check > 0:
                #                 locked_vec = project_point_onto_plane(
                #                     push_vec, pose_bone.z_axis, pose_bone.y_axis)
                #                 push_vec = lerp_vec(push_vec, locked_vec, 0.3)

                #         elif axis_locked == "-Y":
                #             direction_check = pose_bone.y_axis.normalized().dot(push_vec)
                #             if direction_check < 0:
                #                 locked_vec = project_point_onto_plane(
                #                     push_vec, pose_bone.z_axis, pose_bone.y_axis)
                #                 push_vec = lerp_vec(push_vec, locked_vec, 0.3)

                #         elif axis_locked == "+X":
                #             direction_check = pose_bone.x_axis.normalized().dot(push_vec)
                #             if direction_check > 0:
                #                 locked_vec = project_point_onto_plane(
                #                     push_vec, pose_bone.y_axis, pose_bone.x_axis)
                #                 push_vec = lerp_vec(push_vec, locked_vec, 0.3)

                #         elif axis_locked == "-X":
                #             direction_check = pose_bone.x_axis.normalized().dot(push_vec)
                #             if direction_check < 0:
                #                 locked_vec = project_point_onto_plane(
                #                     push_vec, pose_bone.y_axis, pose_bone.x_axis)
                #                 push_vec = lerp_vec(push_vec, locked_vec, 0.3)

                #         elif axis_locked == "+Z":
                #             direction_check = pose_bone.z_axis.normalized().dot(push_vec)
                #             if direction_check > 0:
                #                 locked_vec = project_point_onto_plane(
                #                     push_vec, pose_bone.z_axis, pose_bone.x_axis)
                #                 push_vec = lerp_vec(push_vec, locked_vec, 0.3)

                #         elif axis_locked == "-Z":
                #             direction_check = pose_bone.z_axis.normalized().dot(push_vec)
                #             if direction_check < 0:
                #                 locked_vec = project_point_onto_plane(
                #                     push_vec, pose_bone.z_axis, pose_bone.x_axis)
                #                 push_vec = lerp_vec(push_vec, locked_vec, 0.3)

                #     base_pos_dir += push_vec

            # evaluate mesh collision
            if spring_bone.b_is_bone_colliding:
                BSB_SpringBoneCollisionStep(
                    scene,
                    depsgraph,
                    (pose_bone.tail + pose_bone.head) * 0.5,
                    pose_bone_properties.global_influence,
                    base_pos_dir,
                    pose_bone
                )

                # for mesh in scene.sb_mesh_colliders:
                #     obj = bpy.data.objects.get(mesh.name)
                #     pose_bone_center = (pose_bone.tail + pose_bone.head) * 0.5
                #     col_dir = mathutils.Vector((0.0, 0.0, 0.0))
                #     push_vec = mathutils.Vector((0.0, 0.0, 0.0))

                #     object_eval = obj.evaluated_get(depsgraph)
                #     evaluated_mesh = object_eval.to_mesh(
                #         preserve_all_data_layers=False, depsgraph=depsgraph)
                #     for tri in obj.data.loop_triangles:
                #         tri_coords = []
                #         for vi in tri.vertices:
                #             v_coord = evaluated_mesh.vertices[vi].co
                #             v_coord_global = obj.matrix_world @ v_coord
                #             tri_coords.append(
                #                 [v_coord_global[0], v_coord_global[1], v_coord_global[2]])

                #         tri_array = numpy.array(tri_coords)
                #         P = numpy.array(
                #             [pose_bone_center[0], pose_bone_center[1], pose_bone_center[2]])
                #         dist, p = project_point_onto_tri(tri_array, P)
                #         p = mathutils.Vector((p[0], p[1], p[2]))
                #         collision_dist = obj.sb_collider_dist
                #         repel_force = obj.sb_collider_force

                #         if dist < collision_dist:
                #             col_dir += (pose_bone_center - p)
                #             push_vec = col_dir.normalized() * (collision_dist - dist) * repel_force
                #             base_pos_dir += push_vec * pose_bone.sb_global_influence

        # add velocity
        spring_bone.speed += (
            base_pos_dir *
            pose_bone.bsb_pose_bone_properties.spring_stiffness
        )
        spring_bone.speed *= pose_bone.bsb_pose_bone_properties.spring_dampening_force

        empty_head.location += spring_bone.speed
        # global influence
        empty_head.location = lerp_vec(
            empty_head.location, emp_tail_loc, pose_bone.bsb_pose_bone_properties.global_influence)

    return None


def BSB_SpringBoneCollisionStep(scene: bpy.types.Scene, depsgraph: bpy.types.Depsgraph, bone_center: mathutils.Vector, influence: float, base_pos_dir, pose_bone: bpy.types.PoseBone):
    if (hasattr(scene, "bsb_mesh_colliders")):
        for collider_objects in scene.bsb_mesh_colliders:
            mesh_object = bpy.data.objects.get(collider_objects.name)
            object_eval: bpy.types.Object = mesh_object.evaluated_get(
                depsgraph)

            evaluated_mesh: bpy.types.Mesh = object_eval.to_mesh(
                preserve_all_data_layers=False, depsgraph=depsgraph)

            object_properties: BSB_PG_ObjectProperties = mesh_object.bsb_object_properties

            v_direction = mathutils.Vector((0.0, 0.0, 0.0))
            v_push = mathutils.Vector((0.0, 0.0, 0.0))

            for tri in evaluated_mesh.loop_triangles:
                tri_coords = []
                for vi in tri.vertices:
                    v_coord = evaluated_mesh.vertices[vi].co
                    v_coord_global = object_eval.matrix_world @ v_coord
                    tri_coords.append(
                        [*v_coord_global])

                tri_array = numpy.array(tri_coords)
                P = numpy.array(
                    [*pose_bone.tail])
                dist, p = project_point_onto_tri(tri_array, P)
                p = mathutils.Vector((p))
                collision_dist = object_properties.collider_radius
                repel_force = object_properties.collider_repulsion_force

                if dist < collision_dist:
                    v_direction += (bone_center - p)
                    v_push = v_direction.normalized() * (collision_dist - dist) * repel_force
                    base_pos_dir += v_push * influence


def project_point_onto_plane(point_source, plane_point, plane_normal):
    plane_normal = plane_normal.normalized()
    return point_source - ((point_source - plane_point).dot(plane_normal)) * plane_normal


def project_point_onto_tri(TRI, P):
    # return the distance and the projected surface point
    # between a point and a triangle in 3D
    # original code: https://gist.github.com/joshuashaffer/
    # Author: Gwolyn Fischer

    B = TRI[0, :]
    E0 = TRI[1, :] - B
    # E0 = E0/sqrt(sum(E0.^2)); %normalize vector
    E1 = TRI[2, :] - B
    # E1 = E1/sqrt(sum(E1.^2)); %normalize vector
    D = B - P
    a = numpy.dot(E0, E0)
    b = numpy.dot(E0, E1)
    c = numpy.dot(E1, E1)
    d = numpy.dot(E0, D)
    e = numpy.dot(E1, D)
    f = numpy.dot(D, D)

    # print "{0} {1} {2} ".format(B,E1,E0)
    det = a * c - b * b
    s = b * e - c * d
    t = b * d - a * e

    # Terible tree of conditionals to determine in which region of the diagram
    # shown above the projection of the point into the triangle-plane lies.
    if (s + t) <= det:
        if s < 0.0:
            if t < 0.0:
                # region4
                if d < 0:
                    t = 0.0
                    if -d >= a:
                        s = 1.0
                        sqrdistance = a + 2.0 * d + f
                    else:
                        s = -d / a
                        sqrdistance = d * s + f
                else:
                    s = 0.0
                    if e >= 0.0:
                        t = 0.0
                        sqrdistance = f
                    else:
                        if -e >= c:
                            t = 1.0
                            sqrdistance = c + 2.0 * e + f
                        else:
                            t = -e / c
                            sqrdistance = e * t + f

                            # of region 4
            else:
                # region 3
                s = 0
                if e >= 0:
                    t = 0
                    sqrdistance = f
                else:
                    if -e >= c:
                        t = 1
                        sqrdistance = c + 2.0 * e + f
                    else:
                        t = -e / c
                        sqrdistance = e * t + f
                        # of region 3
        else:
            if t < 0:
                # region 5
                t = 0
                if d >= 0:
                    s = 0
                    sqrdistance = f
                else:
                    if -d >= a:
                        s = 1
                        sqrdistance = a + 2.0 * d + f  # GF 20101013 fixed typo d*s ->2*d
                    else:
                        s = -d / a
                        sqrdistance = d * s + f
            else:
                # region 0
                invDet = 1.0 / det
                s = s * invDet
                t = t * invDet
                sqrdistance = s * (a * s + b * t + 2.0 * d) + \
                    t * (b * s + c * t + 2.0 * e) + f
    else:
        if s < 0.0:
            # region 2
            tmp0 = b + d
            tmp1 = c + e
            if tmp1 > tmp0:  # minimum on edge s+t=1
                numer = tmp1 - tmp0
                denom = a - 2.0 * b + c
                if numer >= denom:
                    s = 1.0
                    t = 0.0
                    sqrdistance = a + 2.0 * d + f  # GF 20101014 fixed typo 2*b -> 2*d
                else:
                    s = numer / denom
                    t = 1 - s
                    sqrdistance = s * (a * s + b * t + 2 * d) + \
                        t * (b * s + c * t + 2 * e) + f

            else:  # minimum on edge s=0
                s = 0.0
                if tmp1 <= 0.0:
                    t = 1
                    sqrdistance = c + 2.0 * e + f
                else:
                    if e >= 0.0:
                        t = 0.0
                        sqrdistance = f
                    else:
                        t = -e / c
                        sqrdistance = e * t + f
                        # of region 2
        else:
            if t < 0.0:
                # region6
                tmp0 = b + e
                tmp1 = a + d
                if tmp1 > tmp0:
                    numer = tmp1 - tmp0
                    denom = a - 2.0 * b + c
                    if numer >= denom:
                        t = 1.0
                        s = 0
                        sqrdistance = c + 2.0 * e + f
                    else:
                        t = numer / denom
                        s = 1 - t
                        sqrdistance = s * \
                            (a * s + b * t + 2.0 * d) + t * \
                            (b * s + c * t + 2.0 * e) + f

                else:
                    t = 0.0
                    if tmp1 <= 0.0:
                        s = 1
                        sqrdistance = a + 2.0 * d + f
                    else:
                        if d >= 0.0:
                            s = 0.0
                            sqrdistance = f
                        else:
                            s = -d / a
                            sqrdistance = d * s + f
            else:
                # region 1
                numer = c + e - b - d
                if numer <= 0:
                    s = 0.0
                    t = 1.0
                    sqrdistance = c + 2.0 * e + f
                else:
                    denom = a - 2.0 * b + c
                    if numer >= denom:
                        s = 1.0
                        t = 0.0
                        sqrdistance = a + 2.0 * d + f
                    else:
                        s = numer / denom
                        t = 1 - s
                        sqrdistance = s * \
                            (a * s + b * t + 2.0 * d) + t * \
                            (b * s + c * t + 2.0 * e) + f

    # account for numerical round-off error
    if sqrdistance < 0:
        sqrdistance = 0

    dist = sqrt(sqrdistance)

    PP0 = B + s * E0 + t * E1
    return dist, PP0
# endregion
# endregion
# endregion
# endregion
# endregion


def project_point_onto_line(a, b, p):
    # project the point p onto the line a,b
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


def lerp_vec(vec_a, vec_b, t):
    return vec_a * t + vec_b * (1 - t)

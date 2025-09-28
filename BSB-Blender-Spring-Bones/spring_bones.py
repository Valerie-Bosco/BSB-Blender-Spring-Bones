from math import sqrt

import bpy
import mathutils
import numpy

from .BSB_Properties import (BSB_PG_PoseBoneProperties, BSB_PG_SceneProperties,
                             BSB_PG_SpringBone)


def lerp_vec(vec_a, vec_b, t):
    return vec_a * t + vec_b * (1 - t)


def get_pose_bone(armature_object: bpy.types.Object, name: str):
    try:
        return armature_object.pose.bones[name]
    except:
        return None


def BSB_SpringBoneSimulationStep(context: bpy.types.Context):
    scene = context.scene
    depsgraph = context.evaluated_depsgraph_get()

    for spring_bone in scene.bsb_spring_bones:
        spring_bone: BSB_PG_SpringBone
        print("simulation step was ran")
        if spring_bone.bone_collider:
            continue

        armature = spring_bone.armature
        pose_bone = armature.pose.bones[spring_bone.name]
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
                pose_bone_collider_radius = pose_bone_collider.collider_radius
                pose_bone_center = (pose_bone.tail + pose_bone.head) * 0.5
                p = project_point_onto_line(
                    pose_bone_collider.head, pose_bone_collider.tail, pose_bone_center)
                col_dir = (pose_bone_center - p)
                dist = col_dir.magnitude

                if dist < pose_bone_collider_radius:
                    push_vec = col_dir.normalized() * (pose_bone_collider_radius - dist) * \
                        pose_bone_collider.sb_collider_force
                    if axis_locked != "NONE" and axis_locked != None:
                        if axis_locked == "+Y":
                            direction_check = pose_bone.y_axis.normalized().dot(push_vec)
                            if direction_check > 0:
                                locked_vec = project_point_onto_plane(
                                    push_vec, pose_bone.z_axis, pose_bone.y_axis)
                                push_vec = lerp_vec(push_vec, locked_vec, 0.3)

                        elif axis_locked == "-Y":
                            direction_check = pose_bone.y_axis.normalized().dot(push_vec)
                            if direction_check < 0:
                                locked_vec = project_point_onto_plane(
                                    push_vec, pose_bone.z_axis, pose_bone.y_axis)
                                push_vec = lerp_vec(push_vec, locked_vec, 0.3)

                        elif axis_locked == "+X":
                            direction_check = pose_bone.x_axis.normalized().dot(push_vec)
                            if direction_check > 0:
                                locked_vec = project_point_onto_plane(
                                    push_vec, pose_bone.y_axis, pose_bone.x_axis)
                                push_vec = lerp_vec(push_vec, locked_vec, 0.3)

                        elif axis_locked == "-X":
                            direction_check = pose_bone.x_axis.normalized().dot(push_vec)
                            if direction_check < 0:
                                locked_vec = project_point_onto_plane(
                                    push_vec, pose_bone.y_axis, pose_bone.x_axis)
                                push_vec = lerp_vec(push_vec, locked_vec, 0.3)

                        elif axis_locked == "+Z":
                            direction_check = pose_bone.z_axis.normalized().dot(push_vec)
                            if direction_check > 0:
                                locked_vec = project_point_onto_plane(
                                    push_vec, pose_bone.z_axis, pose_bone.x_axis)
                                push_vec = lerp_vec(push_vec, locked_vec, 0.3)

                        elif axis_locked == "-Z":
                            direction_check = pose_bone.z_axis.normalized().dot(push_vec)
                            if direction_check < 0:
                                locked_vec = project_point_onto_plane(
                                    push_vec, pose_bone.z_axis, pose_bone.x_axis)
                                push_vec = lerp_vec(push_vec, locked_vec, 0.3)

                    base_pos_dir += push_vec

            # evaluate mesh collision
            if spring_bone.b_is_bone_colliding:
                pass
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


def project_point_onto_plane(q, p, n):
    # q = (vector) point source
    # p = (vector) point belonging to the plane
    # n = (vector) normal of the plane

    n = n.normalized()
    return q - ((q - p).dot(n)) * n


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


def update_bone(self, context: bpy.types.Context):
    armature = context.pose_object
    deps = context.evaluated_depsgraph_get()

    scene_properties = context.scene.bsb_scene_properties
    scene_spring_bones = context.scene.bsb_spring_bones

    for pose_bone in armature.pose.bones:
        if pose_bone.get("b_enable_spring") == False:
            constraint = pose_bone.constraints.get("spring")
            if (constraint is not None):
                pose_bone.constraints.remove(constraint)

    for i in range(0, len(scene_spring_bones)):
        scene_spring_bones.remove(i)

    for pose_bone in armature.pose.bones:

        pose_bone_properties: BSB_PG_PoseBoneProperties = pose_bone.bsb_pose_bone_properties

        is_spring_bone = pose_bone_properties.b_enable_spring
        is_collider_bone = pose_bone_properties.b_enable_as_collider

        rotation_enabled = pose_bone_properties.b_enable_bone_rotation
        b_can_collide = pose_bone_properties.b_should_collide

        if (is_spring_bone or is_collider_bone):
            print(f"{pose_bone} was updated")
            bone_tail = armature.matrix_world @ pose_bone.tail
            bone_head = armature.matrix_world @ pose_bone.head

            item: BSB_PG_SpringBone = scene_spring_bones.add()
            item.name = pose_bone.name
            item.armature = armature
            item.last_location = bone_head

            parent_name = pose_bone.parent.name if pose_bone.parent is not None else ""

            item.bone_collider = is_collider_bone
            item.b_is_bone_colliding = b_can_collide

            empty_radius = 1
            if (is_spring_bone):
                if (bpy.data.objects.get(item.name + '_spring') is None):
                    empty_anchor = bpy.data.objects.new(
                        item.name + '_spring', None
                    )
                    context.scene.collection.objects.link(empty_anchor)
                    empty_anchor.empty_display_size = empty_radius
                    empty_anchor.empty_display_type = 'PLAIN_AXES'
                    empty_anchor.location = bone_tail if rotation_enabled else bone_head
                    empty_anchor.hide_set(True)
                    empty_anchor.hide_select = True

                if (bpy.data.objects.get(item.name + '_spring_tail') is None):
                    empty_anchor_tail = bpy.data.objects.new(
                        item.name + '_spring_tail', None
                    )
                    context.scene.collection.objects.link(
                        empty_anchor_tail
                    )
                    empty_anchor_tail.empty_display_size = empty_radius
                    empty_anchor_tail.empty_display_type = 'PLAIN_AXES'
                    empty_anchor_tail.matrix_world = mathutils.Matrix.Translation(
                        bone_tail if rotation_enabled else bone_head
                    )
                    empty_anchor_tail.hide_set(True)
                    empty_anchor_tail.hide_select = True

                    matrix = empty_anchor_tail.matrix_world.copy()
                    empty_anchor_tail.parent = armature
                    empty_anchor_tail.parent_type = "BONE"
                    empty_anchor_tail.parent_bone = parent_name
                    empty_anchor_tail.matrix_world = matrix

                spring_constraint = pose_bone.constraints.get("spring")
                if (spring_constraint is not None):
                    pose_bone.constraints.remove(spring_constraint)

                constraint = None
                if (pose_bone.bsb_pose_bone_properties.b_enable_bone_rotation):
                    constraint = pose_bone.constraints.new('DAMPED_TRACK')
                    constraint.target = bpy.data.objects[item.name + '_spring']
                else:
                    constraint = pose_bone.constraints.new('COPY_LOCATION')
                    constraint.target = bpy.data.objects[item.name + '_spring']
                constraint.name = 'spring'


def end_spring_bone(self, context: bpy.types.Context):
    scene_properties: BSB_PG_SceneProperties = context.scene.bsb_scene_properties
    if scene_properties.b_global_spring:

        wm: bpy.types.WindowManager = context.window_manager
        wm.event_timer_remove(self.timer_handler)

        scene_properties.b_global_spring = False

    for item in context.scene.bsb_spring_bones:

        active_bone = context.active_object.pose.bones.get(item.name)
        if active_bone == None:
            continue

        cns = active_bone.constraints.get('spring')
        if cns:
            active_bone.constraints.remove(cns)

        emp1 = bpy.data.objects.get(active_bone.name + '_spring')
        emp2 = bpy.data.objects.get(active_bone.name + '_spring_tail')
        if emp1:
            bpy.data.objects.remove(emp1)
        if emp2:
            bpy.data.objects.remove(emp2)

    print("--End--")


class SB_OT_spring_modal(bpy.types.Operator):
    """Spring Bones, interactive mode"""

    bl_idname = "sb.spring_bone"
    bl_label = "spring_bone"

    timer_handler = None

    def terminate_modal(self, context: bpy.types.Context):
        print("TEMINATE WAS RAN")

        if (self.timer_handler is not None):
            wm: bpy.types.WindowManager = context.window_manager
            wm.modal_handler_add
            wm.event_timer_remove(self.timer_handler)

        if (context.scene is not None):
            scene_properties: BSB_PG_SceneProperties = context.scene.bsb_scene_properties
            scene_properties.b_global_spring = False

            if (context.pose_object is not None):
                armature_object: bpy.types.Object = context.pose_object

                for item in context.scene.bsb_spring_bones:
                    active_bone: bpy.types.PoseBone = armature_object.pose.bones.get(
                        item.name
                    )
                    if (active_bone is None):
                        continue

                    constraint = active_bone.constraints.get("spring")
                    if (constraint is not None):
                        active_bone.constraints.remove(constraint)

                    anchor = bpy.data.objects.get(
                        active_bone.name + '_spring'
                    )
                    anchor_tail = bpy.data.objects.get(
                        active_bone.name + '_spring_tail'
                    )
                    if (anchor is not None):
                        bpy.data.objects.remove(anchor)
                    if (anchor_tail is not None):
                        bpy.data.objects.remove(anchor_tail)

            scene_properties.b_global_spring = False
        return {"FINISHED"}

    def modal(self, context, event):
        if (event.type == "ESC") or (context.scene.bsb_scene_properties.b_global_spring == False):
            return self.terminate_modal(context)

        if (event.type == 'TIMER'):
            BSB_SpringBoneSimulationStep(context)

        return {'PASS_THROUGH'}

    def invoke(self, context: bpy.types.Context, event):
        print("INVOKE WAS RAN")
        scene_properties: BSB_PG_SceneProperties = context.scene.bsb_scene_properties

        if (scene_properties.b_global_spring == False):
            wm: bpy.types.WindowManager = context.window_manager
            self.timer_handler = wm.event_timer_add(
                0.02, window=context.window
            )
            wm.modal_handler_add(self)

            scene_properties.b_global_spring = True
            update_bone(self, context)

        else:
            return self.terminate_modal(context)

        return {"RUNNING_MODAL"}


class SB_OT_spring(bpy.types.Operator):
    """Spring Bones, animation mode. Support baking."""

    bl_idname = "sb.spring_bone_frame"
    bl_label = "spring_bone_frame"

    def execute(self, context: bpy.types.Context):
        scene_properties: BSB_PG_SceneProperties = context.scene.bsb_scene_properties

        if (scene_properties.b_global_sim_only_on_frame_change == False):
            scene_properties.b_global_sim_only_on_frame_change = True
            update_bone(self, context)
        else:
            end_spring_bone(self, context)
            scene_properties.b_global_sim_only_on_frame_change = False

        return {'FINISHED'}


class SB_OT_select_bone(bpy.types.Operator):
    """Select this bone"""

    bl_idname = "sb.select_bone"
    bl_label = "select_bone"

    bone_name: bpy.props.StringProperty(default="")  # type:ignore

    def execute(self, context):
        data_bone = get_pose_bone(self.bone_name).bone
        bpy.context.active_object.data.bones.active = data_bone
        data_bone.select = True
        for i, l in enumerate(data_bone.layers):
            if l == True and bpy.context.active_object.data.layers[i] == False:
                bpy.context.active_object.data.layers[i] = True
                # print("enabled layer", i)

        # get_pose_bone(self.bone_name).select = True

        return {'FINISHED'}


###########  UI PANEL  ###################

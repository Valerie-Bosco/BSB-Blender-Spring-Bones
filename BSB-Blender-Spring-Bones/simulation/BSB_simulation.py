import bpy
import mathutils
import numpy

from .BSB_math import lerp_vec, project_point_onto_tri
from ..BSB_Properties import (BSB_PG_PoseBoneProperties, BSB_PG_SpringBone)
from ..spring_bones import project_point_onto_line, project_point_onto_plane


def BSB_SpringBoneSimulationStep(context: bpy.types.Context):
    scene = context.scene
    depsgraph = context.evaluated_depsgraph_get()

    for spring_bone in scene.bsb_spring_bones:
        spring_bone: BSB_PG_SpringBone
        if spring_bone.bone_collider:
            continue

        armature = spring_bone.armature
        pose_bone = armature.pose.bones[spring_bone.name]
        pose_bone_properties: BSB_PG_PoseBoneProperties = pose_bone.bsb_pose_bone_properties

        if pose_bone_properties.global_influence == 0.0:
            continue

        empty_tail = bpy.data.objects.get(spring_bone.name + '_spring_tail')
        empty_head = bpy.data.objects.get(spring_bone.name + '_spring')

        if empty_tail is None or empty_head is None:
            continue

        emp_tail_loc, rot, scale = empty_tail.matrix_world.decompose()

        axis_locked = pose_bone_properties.spring_axis_lock
        base_pos_dir = mathutils.Vector(
            (0, 0, -pose_bone_properties.spring_gravity))
        base_pos_dir += (emp_tail_loc - empty_head.location)

        if spring_bone.b_is_bone_colliding:
            for bone_collider in scene.bsb_spring_bones:
                if not bone_collider.bone_collider:
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

                for mesh in scene.sb_mesh_colliders:
                    obj = bpy.data.objects.get(mesh.name)
                    pose_bone_center = (pose_bone.tail + pose_bone.head) * 0.5
                    col_dir = mathutils.Vector((0.0, 0.0, 0.0))
                    push_vec = mathutils.Vector((0.0, 0.0, 0.0))

                    object_eval = obj.evaluated_get(depsgraph)
                    evaluated_mesh = object_eval.to_mesh(
                        preserve_all_data_layers=False, depsgraph=depsgraph)
                    for tri in obj.data.loop_triangles:
                        tri_coords = []
                        for vi in tri.vertices:
                            v_coord = evaluated_mesh.vertices[vi].co
                            v_coord_global = obj.matrix_world @ v_coord
                            tri_coords.append(
                                [v_coord_global[0], v_coord_global[1], v_coord_global[2]])

                        tri_array = numpy.array(tri_coords)
                        plane_point = numpy.array(
                            [pose_bone_center[0], pose_bone_center[1], pose_bone_center[2]])
                        dist, plane_point = project_point_onto_tri(plane_point, tri_array)
                        plane_point = mathutils.Vector((plane_point[0], plane_point[1], plane_point[2]))
                        collision_dist = obj.sb_collider_dist
                        repel_force = obj.sb_collider_force

                        if dist < collision_dist:
                            col_dir += (pose_bone_center - plane_point)
                            push_vec = col_dir.normalized() * (collision_dist - dist) * repel_force
                            base_pos_dir += push_vec * pose_bone.sb_global_influence

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

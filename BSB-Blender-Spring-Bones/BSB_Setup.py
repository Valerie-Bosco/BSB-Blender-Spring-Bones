import bpy

from .BSB_Properties import (BSB_PG_ObjectProperties,
                             BSB_PG_PoseBoneProperties, BSB_PG_SceneProperties,
                             BSB_PG_SpringBone)

DEBUG = True


def BSB_synchronize_sandbox(context: bpy.types.Context):
    armature = context.pose_object
    scene: bpy.types.Scene = context.scene
    scene_spring_bones: list[BSB_PG_SpringBone] = context.scene.bsb_spring_bones

    # MESH COLLISION
    for scene_object in scene.objects:
        if (not hasattr(scene_object, "bsb_object_properties")):
            continue

        object_properties: BSB_PG_ObjectProperties = scene_object.bsb_object_properties

        if object_properties.b_collider:
            item_mesh_collider = scene.bsb_mesh_colliders.add()
            item_mesh_collider.name = scene_object.name

    # SPRING BONES
    if (armature is not None):
        for pose_bone in armature.pose.bones:
            if pose_bone.get("b_enable_spring") == False:
                constraint = pose_bone.constraints.get("spring")
                if (constraint is not None):
                    pose_bone.constraints.remove(constraint)

    for i in range(0, len(scene_spring_bones)):
        scene_spring_bones.remove(i)

    if (armature is not None):
        for pose_bone in armature.pose.bones:

            pose_bone_properties: BSB_PG_PoseBoneProperties = pose_bone.bsb_pose_bone_properties

            is_spring_bone = pose_bone_properties.b_enable_spring
            # is_collider_bone = pose_bone_properties.b_enable_as_collider

            rotation_enabled = pose_bone_properties.b_enable_bone_rotation
            # b_can_collide = pose_bone_properties.b_should_collide

            if (is_spring_bone):
                bone_head_wco = armature.matrix_world @ pose_bone.head
                bone_tail_wco = armature.matrix_world @ pose_bone.tail

                item: BSB_PG_SpringBone = scene_spring_bones.add()
                item.name = pose_bone.name
                item.armature = armature
                # item.head_frame_wco_pairing =
                # item.last_tail_wco

                # parent_name = pose_bone.parent.name if pose_bone.parent is not None else ""

                # item.bone_collider = is_collider_bone
                # item.b_is_bone_colliding = b_can_collide

                empty_radius = 1
                if (is_spring_bone):
                    scene_spring_bones[pose_bone.name].head_speed = (0, 0, 0)


                    # Head
                    head_anchor: bpy.types.Object = scene.objects.get(
                        item.name + '_spring'
                    )
                    if (head_anchor is None):
                        head_anchor = bpy.data.objects.new(
                            item.name + '_spring', None
                        )
                        context.scene.collection.objects.link(
                            head_anchor
                        )

                    head_anchor.empty_display_size = empty_radius
                    head_anchor.empty_display_type = 'PLAIN_AXES'
                    head_anchor.location = bone_head_wco
                    if (DEBUG == False):
                        head_anchor.hide_set(True)
                        head_anchor.hide_select = True

                    # Tail
                    tail_anchor: bpy.types.Object = bpy.data.objects.get(
                        item.name + '_spring_tail'
                    )
                    if (tail_anchor is None):
                        tail_anchor = bpy.data.objects.new(
                            item.name + '_spring_tail', None
                        )
                        context.scene.collection.objects.link(
                            tail_anchor
                        )

                    tail_anchor.empty_display_size = empty_radius
                    tail_anchor.empty_display_type = 'PLAIN_AXES'
                    tail_anchor.location = bone_tail_wco
                    if (DEBUG == False):
                        tail_anchor.hide_set(True)
                        tail_anchor.hide_select = True

                    # matrix = tail_anchor.matrix_world.copy()
                    # tail_anchor.parent = armature
                    # tail_anchor.parent_type = "BONE"
                    # tail_anchor.parent_bone = parent_name
                    # tail_anchor.matrix_world = matrix

                    spring_constraint = pose_bone.constraints.get("spring")
                    if (spring_constraint is not None):
                        pose_bone.constraints.remove(spring_constraint)

                    constraint = None
                    # if (pose_bone.bsb_pose_bone_properties.b_enable_bone_rotation):
                    constraint = pose_bone.constraints.new('DAMPED_TRACK')
                    constraint.target = scene.objects[
                        item.name +
                        "_spring_tail"
                    ]
                    # else:
                    #     constraint = pose_bone.constraints.new('COPY_LOCATION')
                    #     constraint.target = scene.objects[item.name + '_spring']
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

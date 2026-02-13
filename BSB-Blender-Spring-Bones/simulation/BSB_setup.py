import bpy
import mathutils

from ..BSB_Properties import BSB_PG_PoseBoneProperties, BSB_PG_SceneProperties, BSB_PG_SpringBone


def update_bone(self, context: bpy.types.Context):
    armature = context.pose_object
    deps = context.evaluated_depsgraph_get()
  
    scene_properties = context.scene.bsb_scene_properties
    scene_spring_bones = context.scene.bsb_spring_bones

    for pose_bone in armature.pose.bones:
        if not pose_bone.get("b_enable_spring"):
            constraint = pose_bone.constraints.get("spring")
            if constraint is not None:
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
    if scene_properties.b_async_spring_simulation_running:
        wm: bpy.types.WindowManager = context.window_manager
        wm.event_timer_remove(self.async_sim_timer)

        scene_properties.b_async_spring_simulation_running = False

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

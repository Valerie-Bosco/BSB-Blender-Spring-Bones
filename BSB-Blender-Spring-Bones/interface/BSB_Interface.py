import bpy

from ..spring_bones import SB_OT_select_bone, SB_OT_spring, SB_OT_spring_modal


class SB_PT_ui(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'bone'
    bl_label = "Spring Bones"

    @classmethod
    def poll(cls, context):
        return context.active_object

    def draw(self, context):
        layout = self.layout
        object = context.object

        scene = context.scene
        col = layout.column(align=True)

        if context.mode == "POSE" and bpy.context.active_pose_bone:
            active_bone = bpy.context.active_pose_bone
            # col.label(text='Scene Parameters:')
            col = layout.column(align=True)
            # col.prop(scene, 'sb_global_spring', text="Enable spring")
            if context.scene.sb_global_spring == False:
                col.operator(SB_OT_spring_modal.bl_idname, text="Start - Interactive Mode", icon='PLAY')
            if context.scene.sb_global_spring == True:
                col.operator(SB_OT_spring_modal.bl_idname, text="Stop", icon='PAUSE')

            col.enabled = not context.scene.sb_global_spring_frame

            col = layout.column(align=True)
            if context.scene.sb_global_spring_frame == False:
                col.operator(SB_OT_spring.bl_idname, text="Start - Animation Mode", icon='PLAY')
            if context.scene.sb_global_spring_frame == True:
                col.operator(SB_OT_spring.bl_idname, text="Stop", icon='PAUSE')

            col.enabled = not context.scene.sb_global_spring

            col = layout.column(align=True)

            col.label(text='Bone Parameters:')
            col.prop(active_bone, 'sb_bone_spring', text="Spring")
            col.prop(active_bone, 'sb_bone_rot', text="Rotation")
            col.prop(active_bone, 'sb_stiffness', text="Bouncy")
            col.prop(active_bone, 'sb_damp', text="Speed")
            col.prop(active_bone, 'sb_gravity', text="Gravity")
            col.prop(active_bone, 'sb_global_influence', text="Influence")
            col.prop(active_bone, 'sb_collide', text="Is Colliding")
            col.label(text="Lock axis when colliding:")
            col.prop(active_bone, 'sb_lock_axis', text="")
            col.enabled = not active_bone.sb_bone_collider

            layout.separator()
            col = layout.column(align=True)
            col.prop(active_bone, 'sb_bone_collider', text="Collider")
            col.prop(active_bone, 'sb_collider_dist', text="Collider Distance")
            col.prop(active_bone, 'sb_collider_force', text="Collider Force")
            col.enabled = not active_bone.sb_bone_spring

            layout.separator()
            layout.prop(scene, "sb_show_colliders")
            col = layout.column(align=True)

            if scene.sb_show_colliders:
                for pbone in bpy.context.active_object.pose.bones:
                    if "sb_bone_collider" in pbone.keys():
                        if pbone.sb_bone_collider:
                            row = col.row()
                            row.label(text=pbone.name)
                            r = row.operator(SB_OT_select_bone.bl_idname, text="Select")
                            r.bone_name = pbone.name


class SB_PT_object_ui(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    bl_label = "Spring Bones"

    @classmethod
    def poll(cls, context):
        if context.active_object:
            return context.active_object.type == "MESH"

    def draw(self, context):
        layout = self.layout
        object = context.active_object

        scene = context.scene
        col = layout.column(align=True)

        if context.mode == "OBJECT" and context.active_object:

            if (
                hasattr(context.active_object, "sb_object_collider") and
                hasattr(context.active_object, "sb_collider_dist") and
                hasattr(context.active_object, "sb_collider_force")
            ):

                col = layout.column(align=True)
                col.prop(context.active_object, "sb_object_collider", text="Collider")
                col.prop(context.active_object, "sb_collider_dist", text="Collider Distance")
                col.prop(context.active_object, "sb_collider_force", text="Collider Force")

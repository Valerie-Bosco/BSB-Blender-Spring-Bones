import bpy

from ..BSB_Properties import BSB_PG_SceneProperties
from ..spring_bones import SB_OT_spring_modal


class SB_PT_ui(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'bone'
    bl_label = "Spring Bones"

    @classmethod
    def poll(cls, context):
        return (context is not None) and (context.mode == "POSE") and (context.active_object is not None)

    def draw(self, context):
        layout: bpy.types.UILayout = self.layout.column(align=True)

        if (context.mode == "POSE") and (context.active_pose_bone is not None):
            scene_properties: BSB_PG_SceneProperties = context.scene.bsb_scene_properties

            ui_scene_parameters = layout.column(align=True)

            if (scene_properties.b_global_spring == True):
                ui_scene_parameters.operator(
                    SB_OT_spring_modal.bl_idname,
                    text="Stop",
                    icon="PAUSE"
                )
            else:
                if ((scene_properties.b_global_sim_only_on_frame_change == False)):
                    ui_scene_parameters.operator(
                        SB_OT_spring_modal.bl_idname,
                        text="Start - Interactive Mode",
                        icon="PLAY"
                    )

            # if (scene_properties.b_global_sim_only_on_frame_change == False):
            #     col.operator(SB_OT_spring.bl_idname,
            #                  text="Start - Animation Mode", icon='PLAY')
            # if scene_properties.b_global_sim_only_on_frame_change == True:
            #     col.operator(SB_OT_spring.bl_idname, text="Stop", icon='PAUSE')

            # col.enabled = not context.scene.sb_global_spring

            col = layout.column(align=True)

            col.label(text='Bone Parameters:')
            # col.prop(active_bone, 'sb_bone_spring', text="Spring")
            # col.prop(active_bone, 'sb_bone_rot', text="Rotation")
            # col.prop(active_bone, 'sb_stiffness', text="Bouncy")
            # col.prop(active_bone, 'sb_damp', text="Speed")
            # col.prop(active_bone, 'sb_gravity', text="Gravity")
            # col.prop(active_bone, 'sb_global_influence', text="Influence")
            # col.prop(active_bone, 'sb_collide', text="Is Colliding")
            # col.label(text="Lock axis when colliding:")
            # col.prop(active_bone, 'sb_lock_axis', text="")
            # col.enabled = not active_bone.sb_bone_collider

            layout.separator()
            col = layout.column(align=True)
            # col.prop(active_bone, 'sb_bone_collider', text="Collider")
            # col.prop(active_bone, 'sb_collider_dist', text="Collider Distance")
            # col.prop(active_bone, 'sb_collider_force', text="Collider Force")
            # # col.enabled = not active_bone.sb_bone_spring

            layout.separator()
            # layout.prop(scene, "sb_show_colliders")
            col = layout.column(align=True)

            # if scene.sb_show_colliders:
            #     for pbone in bpy.context.active_object.pose.bones:
            #         if "sb_bone_collider" in pbone.keys():
            #             if pbone.sb_bone_collider:
            #                 row = col.row()
            #                 row.label(text=pbone.name)
            #                 r = row.operator(SB_OT_select_bone.bl_idname, text="Select")
            #                 r.bone_name = pbone.name


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
                col.prop(context.active_object,
                         "sb_object_collider", text="Collider")
                col.prop(context.active_object, "sb_collider_dist",
                         text="Collider Distance")
                col.prop(context.active_object,
                         "sb_collider_force", text="Collider Force")

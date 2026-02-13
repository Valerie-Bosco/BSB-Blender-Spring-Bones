import bpy

from ..BSB_Operators import BSB_OT_BakeAnimationToAction
from ..BSB_Properties import BSB_PG_SceneProperties
from ..simulation.BSB_operators import BSB_OT_ASyncSpringSimulation, BSB_OT_FrameSyncSpringSimulation


class BSB_PT_UI(bpy.types.Panel):
    bl_label = "Spring Bones"
    bl_idname = "BSB_PT_ui"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bl_category = "BSB"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        ui_layout: bpy.types.UILayout = self.layout.column(align=True)

        ui_bsb_pose_panel: bpy.types.UILayout = ui_layout.column(align=True)
        ui_bsb_pose_panel.enabled = True if (
                (context is not None) and
                (context.mode == "POSE") and
                context.active_object is not None) else False

        scene_properties: BSB_PG_SceneProperties = context.scene.bsb_scene_properties
        # pose_bone_properties: BSB_PG_PoseBoneProperties = context.active_pose_bone.bsb_pose_bone_properties

        ui_scene_parameters = ui_bsb_pose_panel.column(align=True)

        if scene_properties.b_async_spring_simulation_running == False and scene_properties.b_framesync_spring_simulation_running == False:
            ui_scene_parameters.operator(
                BSB_OT_ASyncSpringSimulation.bl_idname,
                text="Start - Interactive Mode",
                icon="PLAY"
            )

            # ui_scene_parameters.operator(
            #     operators.SB_OT_spring.bl_idname,
            #     text="Start - Animation Mode",
            #     icon="PLAY"
            # )

        if scene_properties.b_async_spring_simulation_running:
            ui_scene_parameters.operator(
                BSB_OT_ASyncSpringSimulation.bl_idname,
                text="Stop",
                icon="PAUSE"
            )

        if scene_properties.b_framesync_spring_simulation_running:
            ui_scene_parameters.operator(
                BSB_OT_FrameSyncSpringSimulation.bl_idname,
                text="Stop",
                icon="PAUSE"
            )

        bake_button = ui_bsb_pose_panel.operator(
            BSB_OT_BakeAnimationToAction.bl_idname,
            text="Bake to action"
        )

        ui_bone_parameters = ui_bsb_pose_panel.column(align=True)
        # ui_bone_parameters.label(
        #     text=f"Bone Parameters: [{context.active_pose_bone.name}]")

        # ui_bone_parameters.prop(
        #     pose_bone_properties, "b_enable_spring", text="Spring"
        # )
        # ui_bone_parameters.prop(
        #     pose_bone_properties, "b_enable_bone_rotation", text="Fixed position [rotation mode]"
        # )
        # ui_bone_parameters.prop(
        #     pose_bone_properties, "spring_stiffness", text="Stiffness"
        # )
        # ui_bone_parameters.prop(
        #     pose_bone_properties, "spring_dampening_force", text="Dampening force"
        # )
        # ui_bone_parameters.prop(
        #     pose_bone_properties, "spring_gravity", text="Gravity"
        # )
        # ui_bone_parameters.prop(
        #     pose_bone_properties, "global_influence", text="Influence"
        # )
        #
        # ui_bone_parameters.separator()
        #
        # ui_bone_parameters.prop(
        #     pose_bone_properties, "b_enable_as_collider", text="Is collider"
        # )
        # ui_bone_parameters.prop(
        #     pose_bone_properties, "b_should_collide", text="Should collide"
        # )
        # ui_bone_parameters.prop(
        #     pose_bone_properties, "collider_radius", text="Collider Distance"
        # )
        # ui_bone_parameters.prop(
        #     pose_bone_properties, "collider_repulsion_force", text="Collider Force"
        # )
        #
        # ui_bone_parameters.label(text="Lock axis when colliding:")
        # ui_bone_parameters.prop(
        #     pose_bone_properties, "spring_axis_lock", text=""
        # )

        ui_bsb_pose_panel.separator()
        # ui_bsb_pose_panel.prop(scene, "sb_show_colliders")
        col = ui_bsb_pose_panel.column(align=True)

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
                col.prop(
                    context.active_object,
                    "sb_object_collider", text="Collider"
                )
                col.prop(
                    context.active_object,
                    "sb_collider_dist", text="Collider Distance"

                )
                col.prop(
                    context.active_object,
                    "sb_collider_force", text="Collider Force"
                )

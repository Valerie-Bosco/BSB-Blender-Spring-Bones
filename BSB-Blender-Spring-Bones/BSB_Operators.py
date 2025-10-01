import bpy


class BSB_OT_BakeAnimationToAction(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "bsb.operator_bake_animation_to_action"

    bl_options = {"UNDO"}

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context: bpy.types.Context):
        scene: bpy.types.Scene = context.scene

        bpy.ops.nla.bake(
            frame_start=scene.frame_current,
            frame_end=scene.frame_end,
            step=scene.frame_step,
            only_selected=False,
            visual_keying=True,
            clear_constraints=False,
            clear_parents=False,
            use_current_action=False,
            clean_curves=False,
            bake_types={"POSE"}
        )
        return {"FINISHED"}



import bpy

from .BSB_Properties import BSB_PG_SceneProperties
from .BSB_Setup import BSB_synchronize_sandbox, end_spring_bone
from .BSB_Simulation import BSB_SpringBoneSimulationStep


from .modules.ALXAddonUpdater.ALXAddonUpdater.ALX_AddonUpdater import
class SB_OT_spring_modal(bpy.types.Operator):
    """Spring Bones, interactive mode"""

    bl_idname = "sb.spring_bone"
    bl_label = "spring_bone"

    timer_handler = None
    timer_rate = 0.0
    timer_wait = 0.0

    def terminate_modal(self, context: bpy.types.Context):
        if (self.timer_handler is not None):
            wm: bpy.types.WindowManager = context.window_manager
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
        scene_properties: BSB_PG_SceneProperties = context.scene.bsb_scene_properties
        scene: bpy.types.Scene = context.scene

        if (scene_properties.b_global_spring == False):
            wm: bpy.types.WindowManager = context.window_manager

            self.timer_rate = 1 / (scene.render.fps if scene_properties.b_use_scene_framerate
                                   else scene_properties.custom_framerate)

            self.timer_handler = wm.event_timer_add(
                self.timer_rate,
                window=context.window
            )
            wm.modal_handler_add(self)

            scene_properties.b_global_spring = True
            BSB_synchronize_sandbox(context)

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
            BSB_synchronize_sandbox(context)
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

        # get_pose_bone(self.bone_name).select = True

        return {'FINISHED'}


###########  UI PANEL  ###################

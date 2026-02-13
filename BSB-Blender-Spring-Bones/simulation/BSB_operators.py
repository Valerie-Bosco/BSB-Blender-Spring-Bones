import bpy

from .BSB_setup import end_spring_bone, update_bone
from .BSB_simulation import BSB_SpringBoneSimulationStep
from ..BSB_Properties import (BSB_PG_SceneProperties)


class BSB_OT_ASyncSpringSimulation(bpy.types.Operator):
    """"""

    bl_label = "ASync Spring Simulation"
    bl_idname = "sb.spring_bone"

    async_sim_timer = None

    def terminate_modal(self, context: bpy.types.Context):
        if self.async_sim_timer is not None:
            context.window_manager.event_timer_remove(self.async_sim_timer)

        if context.scene is not None:
            scene_properties: BSB_PG_SceneProperties = context.scene.bsb_scene_properties
            scene_properties.b_async_spring_simulation_running = False

            if context.pose_object is not None:
                armature_object: bpy.types.Object = context.pose_object

                for sb_item in context.scene.bsb_spring_bones:
                    try:
                        active_bone: bpy.types.PoseBone = armature_object.pose.bones[
                            sb_item.name
                        ]
                        constraint = active_bone.constraints.get("spring")
                        if constraint is not None:
                            active_bone.constraints.remove(constraint)

                        anchor = bpy.data.objects.get(
                            active_bone.name + '_spring'
                        )
                        anchor_tail = bpy.data.objects.get(
                            active_bone.name + '_spring_tail'
                        )

                        if anchor is not None:
                            bpy.data.objects.remove(anchor)
                        if anchor_tail is not None:
                            bpy.data.objects.remove(anchor_tail)

                    except NameError:
                        continue
                    except Exception as error:
                        print(error)
                        continue

        return {"FINISHED"}

    def modal(self, context, event):
        if (event.type == "ESC") or (context.scene.bsb_scene_properties.b_async_spring_simulation_running == False):
            return self.terminate_modal(context)

        if event.type == "TIMER":
            BSB_SpringBoneSimulationStep(context)

        return {'PASS_THROUGH'}

    def invoke(self, context: bpy.types.Context, event):
        scene_properties: BSB_PG_SceneProperties = context.scene.bsb_scene_properties

        if not scene_properties.b_async_spring_simulation_running:
            wm: bpy.types.WindowManager = context.window_manager
            self.async_sim_timer = wm.event_timer_add(
                0.02, window=context.window
            )
            wm.modal_handler_add(self)

            scene_properties.b_async_spring_simulation_running = True
            update_bone(self, context)

        else:
            return self.terminate_modal(context)

        return {"RUNNING_MODAL"}


class BSB_OT_FrameSyncSpringSimulation(bpy.types.Operator):
    """"""

    bl_idname = "sb.spring_bone_frame"
    bl_label = "spring_bone_frame"

    def execute(self, context: bpy.types.Context):
        scene_properties: BSB_PG_SceneProperties = context.scene.bsb_scene_properties

        if not scene_properties.b_framesync_spring_simulation_running:
            scene_properties.b_framesync_spring_simulation_running = True
            update_bone(self, context)
        else:
            end_spring_bone(self, context)
            scene_properties.b_framesync_spring_simulation_running = False

        return {'FINISHED'}

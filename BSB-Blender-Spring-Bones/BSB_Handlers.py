import bpy

from .spring_bones import BSB_SpringBoneSimulationStep


@bpy.app.handlers.persistent
def BSB_FrameChangePost(scene, depsgraph):
    BSB_LAMBDA_FrameChangePost(scene, depsgraph)


def BSB_LAMBDA_FrameChangePost(scene, depsgraph):
    if (scene.bsb_scene_properties.b_global_sim_only_on_frame_change == True):
        BSB_SpringBoneSimulationStep(bpy.context)

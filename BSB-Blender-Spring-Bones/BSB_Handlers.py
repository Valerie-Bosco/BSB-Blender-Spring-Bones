import bpy

from .simulation import BSB_simulation


@bpy.app.handlers.persistent
def BSB_FrameChangePost(scene, depsgraph):
    BSB_LAMBDA_FrameChangePost(scene, depsgraph)


def BSB_LAMBDA_FrameChangePost(scene, depsgraph):
    if scene.bsb_scene_properties.b_framesync_spring_simulation_running:
        BSB_simulation.BSB_SpringBoneSimulationStep(bpy.context)

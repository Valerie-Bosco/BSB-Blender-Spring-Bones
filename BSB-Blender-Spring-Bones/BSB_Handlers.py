import bpy

from .spring_bones import BSB_SpringBoneSimulationStep


@bpy.app.handlers.persistent
def BSB_FrameChangePost(scene, depsgraph):
    BSB_LAMBDA_FrameChangePost(scene, depsgraph)


def BSB_LAMBDA_FrameChangePost(scene, depsgraph):
    if (scene.sb_global_spring_frame == True):
        BSB_SpringBoneSimulationStep(scene, depsgraph)

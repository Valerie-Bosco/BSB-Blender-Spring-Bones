import bpy

from .spring_bones import spring_bone


@bpy.app.handlers.persistent
def spring_bone_frame_mode(foo):
    if bpy.context.scene.sb_global_spring_frame == True:
        spring_bone(foo)

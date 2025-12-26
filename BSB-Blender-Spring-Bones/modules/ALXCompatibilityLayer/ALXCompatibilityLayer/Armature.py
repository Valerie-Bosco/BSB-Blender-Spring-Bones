import bpy


def get_pose_bone(armature_object: bpy.types.Object, name: str):
    try:
        return armature_object.pose.bones[name]
    except:
        return None
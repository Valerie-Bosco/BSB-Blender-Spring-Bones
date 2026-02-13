import bpy


def get_pose_bone(armature_object: bpy.types.Object, name: str):
    try:
        return armature_object.pose.bones[name]
    except NameError:
        return None
    except Exception as error:
        print(error)
        return None


class SB_OT_select_bone(bpy.types.Operator):
    """Select this bone"""

    bl_idname = "sb.select_bone"
    bl_label = "select_bone"

    bone_name: bpy.props.StringProperty(default="")  # type:ignore

    def execute(self, context):
        armature_object = None
        data_bone = get_pose_bone(armature_object, self.bone_name).bone
        bpy.context.active_object.data.bones.active = data_bone
        data_bone.select = True
        for i, l in enumerate(data_bone.layers):
            if l == True and bpy.context.active_object.data.layers[i] == False:
                bpy.context.active_object.data.layers[i] = True

        # get_pose_bone(self.bone_name).select = True

        return {'FINISHED'}

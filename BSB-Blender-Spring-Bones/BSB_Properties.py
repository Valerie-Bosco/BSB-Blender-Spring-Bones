import bpy
import mathutils


class bones_collec(bpy.types.PropertyGroup):
    armature: bpy.props.StringProperty(default="")  # type:ignore
    last_loc: bpy.props.FloatVectorProperty(name="Loc", subtype='DIRECTION', default=(0, 0, 0), size=3)  # type:ignore
    speed: bpy.props.FloatVectorProperty(name="Speed", subtype='DIRECTION', default=(0, 0, 0), size=3)  # type:ignore
    dist: bpy.props.FloatProperty(name="distance", default=1.0)  # type:ignore
    target_offset: bpy.props.FloatVectorProperty(name="TargetLoc", subtype='DIRECTION', default=(0, 0, 0), size=3)  # type:ignore
    sb_bone_rot: bpy.props.BoolProperty(name="Bone Rot", default=False)  # type:ignore
    sb_bone_collider: bpy.props.BoolProperty(name="Bone collider", default=False)  # type:ignore
    sb_bone_colliding: bpy.props.BoolProperty(name="Bone colliding", default=True)  # type:ignore
    sb_collider_dist: bpy.props.FloatProperty(name="Bone collider distance", default=0.5)  # type:ignore
    sb_collider_force: bpy.props.FloatProperty(name="Bone collider force", default=1.0)  # type:ignore
    matrix_offset = mathutils.Matrix()
    initial_matrix = mathutils.Matrix()


class mesh_collec(bpy.types.PropertyGroup):
    test: bpy.props.StringProperty(default="")  # type:ignore

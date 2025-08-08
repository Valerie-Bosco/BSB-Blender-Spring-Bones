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


class mesh_collec(bpy.types.PropertyGroup):
    test: bpy.props.StringProperty(default="")  # type:ignore


def BSB_RegisterProperties():
    bpy.types.Scene.sb_spring_bones = bpy.props.CollectionProperty(type=bones_collec)
    bpy.types.Scene.sb_mesh_colliders = bpy.props.CollectionProperty(type=mesh_collec)
    bpy.types.Scene.sb_global_spring = bpy.props.BoolProperty(name="Enable spring", default=False)  # , update=update_global_spring)
    bpy.types.Scene.sb_global_spring_frame = bpy.props.BoolProperty(name="Enable Spring", description="Enable Spring on frame change only", default=False)
    bpy.types.Scene.sb_show_colliders = bpy.props.BoolProperty(name="Show Colliders", description="Show active colliders names", default=False)
    bpy.types.PoseBone.sb_bone_spring = bpy.props.BoolProperty(name="Enabled", default=False, description="Enable spring effect on this bone")
    bpy.types.PoseBone.sb_bone_collider = bpy.props.BoolProperty(name="Collider", default=False, description="Enable this bone as collider")
    bpy.types.PoseBone.sb_collider_dist = bpy.props.FloatProperty(name="Collider Distance", default=0.5, description="Minimum distance to handle collision between the spring and collider bones")
    bpy.types.PoseBone.sb_collider_force = bpy.props.FloatProperty(name="Collider Force", default=1.0, description="Amount of repulsion force when colliding")
    bpy.types.PoseBone.sb_stiffness = bpy.props.FloatProperty(name="Stiffness", default=0.5, min=0.01, max=1.0, description="Bouncy/elasticity value, higher values lead to more bounciness")
    bpy.types.PoseBone.sb_damp = bpy.props.FloatProperty(name="Damp", default=0.7, min=0.0, max=10.0, description="Speed/damping force applied to the bone to go back to it initial position")
    bpy.types.PoseBone.sb_gravity = bpy.props.FloatProperty(name="Gravity", description="Additional vertical force to simulate gravity", default=0.0, min=-100.0, max=100.0)
    bpy.types.PoseBone.sb_bone_rot = bpy.props.BoolProperty(name="Rotation", default=False, description="The spring effect will apply on the bone rotation instead of location")
    bpy.types.PoseBone.sb_lock_axis = bpy.props.EnumProperty(items=(('NONE', 'None', ""), ('+X', '+X', ''), ('-X', '-X', ''), ('+Y', "+Y", ""), ('-Y', '-Y', ""), ('+Z', '+Z', ""), ('-Z', '-Z', '')), default="NONE")
    bpy.types.Object.sb_object_collider = bpy.props.BoolProperty(name="Collider", default=False, description="Enable this bone as collider")
    bpy.types.Object.sb_collider_dist = bpy.props.FloatProperty(name="Collider Distance", default=0.5, description="Minimum distance to handle collision between the spring and collider bones")
    bpy.types.Object.sb_collider_force = bpy.props.FloatProperty(name="Collider Force", default=1.0, description="Amount of repulsion force when colliding")
    bpy.types.PoseBone.sb_collide = bpy.props.BoolProperty(name="Colliding", default=True, description="The bone will collide with other colliders")  # , update=update_global_spring)
    bpy.types.PoseBone.sb_global_influence = bpy.props.FloatProperty(name="Influence", default=1.0, min=0.0, max=1.0, description="Global influence of spring motion")  # , update=update_global_spring)


def BSB_UnregisterProperties():
    del bpy.types.Scene.sb_spring_bones
    del bpy.types.Scene.sb_mesh_colliders
    del bpy.types.Scene.sb_global_spring
    del bpy.types.Scene.sb_global_spring_frame
    del bpy.types.Scene.sb_show_colliders
    del bpy.types.PoseBone.sb_bone_spring
    del bpy.types.PoseBone.sb_bone_collider
    del bpy.types.PoseBone.sb_collider_dist
    del bpy.types.PoseBone.sb_collider_force
    del bpy.types.PoseBone.sb_stiffness
    del bpy.types.PoseBone.sb_damp
    del bpy.types.PoseBone.sb_gravity
    del bpy.types.PoseBone.sb_bone_rot
    del bpy.types.PoseBone.sb_lock_axis
    del bpy.types.Object.sb_object_collider
    del bpy.types.Object.sb_collider_dist
    del bpy.types.Object.sb_collider_force
    del bpy.types.PoseBone.sb_collide
    del bpy.types.PoseBone.sb_global_influence

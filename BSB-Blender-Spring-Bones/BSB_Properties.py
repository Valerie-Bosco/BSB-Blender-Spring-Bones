import bpy


class BSB_PG_ObjectProperties(bpy.types.PropertyGroup):
    b_collider: bpy.props.BoolProperty(name="", default=False)  # type:ignore
    collider_radius: bpy.props.FloatProperty(
        name="Collider Distance",
        default=0.5,
        description="Minimum distance to handle collision between the spring and collider bones"
    )  # type:ignore
    collider_repulsion_force: bpy.props.FloatProperty(
        name="Collider Force",
        default=1.0,
        description="Amount of repulsion force when colliding"
    )  # type:ignore


class BSB_PG_PoseBoneProperties(bpy.types.PropertyGroup):
    global_influence: bpy.props.FloatProperty(
        name="Influence",
        default=1.0,
        min=0.0, max=1.0,
        description="Global influence of spring motion"
    )  # type:ignore

    b_enable_spring: bpy.props.BoolProperty(
        name="Enabled",
        default=False,
        description="Enable spring effect on this bone"
    )  # type:ignore
    b_enable_bone_rotation: bpy.props.BoolProperty(
        name="Bone Rotation",
        default=False
    )  # type:ignore
    spring_stiffness: bpy.props.FloatProperty(
        name="Stiffness",
        default=0.5,
        min=0.01, max=1.0,
        description="Bouncy/elasticity value, higher values lead to more bounciness"
    )  # type:ignore
    spring_dampening_force: bpy.props.FloatProperty(
        name="Damp",
        default=0.7,
        min=0.0, max=10.0,
        description="Speed/damping force applied to the bone to go back to it initial position"
    )  # type:ignore
    spring_gravity: bpy.props.FloatProperty(
        name="Gravity",
        description="Additional vertical force to simulate gravity",
        default=0.0,
        min=-100.0, max=100.0
    )  # type:ignore
    spring_axis_lock: bpy.props.EnumProperty(
        items=(('NONE', 'None', ""),
               ('+X', '+X', ''),
               ('-X', '-X', ''),
               ('+Y', "+Y", ""),
               ('-Y', '-Y', ""),
               ('+Z', '+Z', ""),
               ('-Z', '-Z', '')),
        default="NONE"
    )  # type:ignore

    b_enable_as_collider: bpy.props.BoolProperty(
        name="Collider",
        default=False,
        description="Enable this bone as collider")  # type:ignore
    b_should_collide: bpy.props.BoolProperty(
        name="should collide",
        default=True,
        description="The bone will collide with other colliders"
    )  # type:ignore


class BSB_PG_SpringBone(bpy.types.PropertyGroup):
    armature: bpy.props.PointerProperty(type=bpy.types.Object)  # type:ignore
    last_location: bpy.props.FloatVectorProperty(
        name="Loc",
        subtype='DIRECTION',
        default=(0, 0, 0),
        size=3
    )  # type:ignore
    speed: bpy.props.FloatVectorProperty(
        name="Speed",
        subtype='DIRECTION',
        default=(0, 0, 0),
        size=3
    )  # type:ignore
    distance: bpy.props.FloatProperty(
        name="distance",
        default=1.0
    )  # type:ignore
    target_offset: bpy.props.FloatVectorProperty(
        name="TargetLoc",
        subtype='DIRECTION',
        default=(0, 0, 0),
        size=3
    )  # type:ignore
    bone_collider: bpy.props.BoolProperty(
        name="Bone collider",
        default=False
    )  # type:ignore
    b_is_bone_colliding: bpy.props.BoolProperty(
        name="Bone colliding",
        default=True
    )  # type:ignore
    collider_radius: bpy.props.FloatProperty(
        name="Bone collider distance",
        default=0.5
    )  # type:ignore
    sb_collider_force: bpy.props.FloatProperty(
        name="Bone collider force",
        default=1.0
    )  # type:ignore

    b_enable_as_collider: bpy.props.BoolProperty(
        name="Collider",
        default=False,
        description="Enable this bone as collider"
    )  # type:ignore
    collider_radius: bpy.props.FloatProperty(
        name="Collider Distance",
        default=0.5,
        description="Minimum distance to handle collision between the spring and collider bones")  # type:ignore
    collider_repulsion_force: bpy.props.FloatProperty(
        name="Collider Force",
        default=1.0,
        description="Amount of repulsion force when colliding"
    )  # type:ignore


class BSB_PG_MeshColliders(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="", default="")  # type:ignore


class BSB_PG_SceneProperties(bpy.types.PropertyGroup):
    b_global_spring: bpy.props.BoolProperty(
        name="Enable spring",
        default=False
    )  # type:ignore
    b_global_sim_only_on_frame_change: bpy.props.BoolProperty(
        name="Enable Spring",
        description="Enable Spring on frame change only",
        default=False
    )  # type:ignore
    b_show_colliders: bpy.props.BoolProperty(
        name="Show Colliders",
        description="Show active colliders names",
        default=False
    )  # type:ignore

    b_use_scene_framerate: bpy.props.BoolProperty(
        name="",
        default=True
    )  # type:ignore

    custom_framerate: bpy.props.FloatProperty(
        name="",
        default=24.0,
        min=1.0,
        max=240.0
    )  # type:ignore


def BSB_RegisterProperties():
    bpy.types.Scene.bsb_scene_properties = bpy.props.PointerProperty(
        type=BSB_PG_SceneProperties
    )

    bpy.types.PoseBone.bsb_pose_bone_properties = bpy.props.PointerProperty(
        type=BSB_PG_PoseBoneProperties
    )
    bpy.types.Object.bsb_object_properties = bpy.props.PointerProperty(
        type=BSB_PG_ObjectProperties
    )

    bpy.types.Scene.bsb_spring_bones = bpy.props.CollectionProperty(
        type=BSB_PG_SpringBone
    )
    bpy.types.Scene.bsb_mesh_colliders = bpy.props.CollectionProperty(
        type=BSB_PG_MeshColliders
    )

    bpy.types.WindowManager.bsb_collision_rendering = {
        "handler": None,
        "shader": None,
        "batch": None
    }


def BSB_UnregisterProperties():
    del bpy.types.Scene.bsb_scene_properties

    del bpy.types.PoseBone.bsb_pose_bone_properties
    del bpy.types.Object.bsb_object_properties

    del bpy.types.Scene.bsb_spring_bones
    del bpy.types.Scene.bsb_mesh_colliders

    del bpy.types.WindowManager.bsb_collision_rendering

import bpy
import mathutils


class BSB_PG_ObjectProperties(bpy.types.PropertyGroup):
    b_collider: bpy.props.BoolProperty(name="", default=False)  # type:ignore
    collider_radius: bpy.props.FloatProperty(# type:ignore
        name="Collider Distance",
        default=0.5,
        description="Minimum distance to handle collision between the spring and collider bones"
    )  # type:ignore
    collider_repulsion_force: bpy.props.FloatProperty(# type:ignore
        name="Collider Force",
        default=1.0,
        description="Amount of repulsion force when colliding"
    )  # type:ignore


class BSB_PG_PoseBoneProperties(bpy.types.PropertyGroup):
    global_influence: bpy.props.FloatProperty(# type:ignore
        name="Influence",
        default=1.0,
        min=0.0, max=1.0,
        description="Global influence of spring motion"
    )  # type:ignore

    b_enable_spring: bpy.props.BoolProperty(# type:ignore
        name="Enabled",
        default=False,
        description="Enable spring effect on this bone"
    )  # type:ignore
    b_enable_bone_rotation: bpy.props.BoolProperty(# type:ignore
        name="Bone Rotation",
        default=False
    )  # type:ignore
    spring_stiffness: bpy.props.FloatProperty(# type:ignore
        name="Stiffness",
        default=0.5,
        min=0.01, max=1.0,
        description="Bouncy/elasticity value, higher values lead to more bounciness"
    )  # type:ignore
    spring_dampening_force: bpy.props.FloatProperty(# type:ignore
        name="Damp",
        default=0.7,
        min=0.0, max=10.0,
        description="Speed/damping force applied to the bone to go back to it initial position"
    )  # type:ignore

    spring_gravity: bpy.props.FloatProperty( # type:ignore
        name="Gravity",
        description="Additional vertical force to simulate gravity",
        default=9.81,
        min=-100.0, max=100.0
    )  # type:ignore
    spring_gravity_vector: bpy.props.FloatVectorProperty( # type:ignore
        name="Gravity Direction",
        description="The direction of gravity",
        default=(0, 0, 1),
        min=-1, max=1
    )  # type:ignore

    spring_tail_mass: bpy.props.FloatProperty(# type:ignore
        name="Mass",
        description="Mass in grams",
        default=50.0,
        min=10.0
    )  # type:ignore

    spring_axis_lock: bpy.props.EnumProperty(# type:ignore
        items=(('NONE', 'None', ""),
               ('+X', '+X', ''),
               ('-X', '-X', ''),
               ('+Y', "+Y", ""),
               ('-Y', '-Y', ""),
               ('+Z', '+Z', ""),
               ('-Z', '-Z', '')),
        default="NONE"
    )  # type:ignore

    b_enable_as_collider: bpy.props.BoolProperty(# type:ignore
        name="Collider",
        default=False,
        description="Enable this bone as collider")  # type:ignore
    b_should_collide: bpy.props.BoolProperty(# type:ignore
        name="should collide",
        default=True,
        description="The bone will collide with other colliders"
    )  # type:ignore


class BSB_PG_SpringBone(bpy.types.PropertyGroup):
    armature: bpy.props.PointerProperty(type=bpy.types.Object)  # type:ignore

    # region INTER MODE ONLY
    last_head_location: bpy.props.FloatVectorProperty(# type:ignore
        name="",
        subtype='DIRECTION',
        default=(0, 0, 0),
        size=3
    )  # type:ignore
    last_tail_location: bpy.props.FloatVectorProperty(# type:ignore
        name="Speed",
        subtype='DIRECTION',
        default=(0, 0, 0),
        size=3
    )  # type:ignore
    # endregion

    # region ANIM MODE ONLY

    # frame:wco
    head_frame_wco_pairing: dict[int,mathutils.Vector]
    tail_frame_wco_pairing: dict[int,mathutils.Vector]

    # endregion

    head_speed: bpy.props.FloatVectorProperty(# type:ignore
        name="Speed",
        subtype='DIRECTION',
        default=(0, 0, 0),
        size=3
    )  # type:ignore
    tail_speed: bpy.props.FloatVectorProperty(# type:ignore
        name="Speed",
        subtype='DIRECTION',
        default=(0, 0, 0),
        size=3
    )  # type:ignore

    distance: bpy.props.FloatProperty(# type:ignore
        name="distance",
        default=1.0
    )  # type:ignore
    target_offset: bpy.props.FloatVectorProperty(# type:ignore
        name="TargetLoc",
        subtype='DIRECTION',
        default=(0, 0, 0),
        size=3
    )  # type:ignore
    bone_collider: bpy.props.BoolProperty(# type:ignore
        name="Bone collider",
        default=False
    )  # type:ignore
    b_is_bone_colliding: bpy.props.BoolProperty(# type:ignore
        name="Bone colliding",
        default=True
    )  # type:ignore
    collider_radius: bpy.props.FloatProperty(# type:ignore
        name="Bone collider distance",
        default=0.5
    )  # type:ignore
    sb_collider_force: bpy.props.FloatProperty(# type:ignore
        name="Bone collider force",
        default=1.0
    )  # type:ignore

    b_enable_as_collider: bpy.props.BoolProperty(# type:ignore
        name="Collider",
        default=False,
        description="Enable this bone as collider"
    )  # type:ignore
    collider_radius: bpy.props.FloatProperty(# type:ignore
        name="Collider Distance",
        default=0.5,
        description="Minimum distance to handle collision between the spring and collider bones")  # type:ignore
    collider_repulsion_force: bpy.props.FloatProperty(# type:ignore
        name="Collider Force",
        default=1.0,
        description="Amount of repulsion force when colliding"
    )  # type:ignore


class BSB_PG_MeshColliders(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="", default="")  # type:ignore


class BSB_PG_SceneProperties(bpy.types.PropertyGroup):
    simulation_scene: bpy.props.PointerProperty(# type:ignore
        type=bpy.types.Scene
    )  # type:ignore

    b_global_spring: bpy.props.BoolProperty(# type:ignore
        name="Enable spring",
        default=False
    )  # type:ignore
    b_global_sim_only_on_frame_change: bpy.props.BoolProperty(# type:ignore
        name="Enable Spring",
        description="Enable Spring on frame change only",
        default=False
    )  # type:ignore
    b_show_colliders: bpy.props.BoolProperty(# type:ignore
        name="Show Colliders",
        description="Show active colliders names",
        default=False
    )  # type:ignore

    b_use_scene_framerate: bpy.props.BoolProperty(# type:ignore
        name="",
        default=True
    )  # type:ignore

    custom_framerate: bpy.props.FloatProperty(# type:ignore
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

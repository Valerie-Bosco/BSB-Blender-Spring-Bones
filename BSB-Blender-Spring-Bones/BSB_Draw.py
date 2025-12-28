import bmesh
import bpy
import gpu
import gpu_extras

from .BSB_Properties import BSB_PG_ObjectProperties
from .BSB_Setup import BSB_synchronize_sandbox


def _BuildVisualCollision(scene: bpy.types.Scene, depsgraph: bpy.types.Depsgraph):
    tri_pack_objects = dict()
    if (hasattr(scene, "bsb_mesh_colliders")):

        for collider_data in scene.bsb_mesh_colliders:
            collider_object: bpy.types.Object = bpy.data.objects.get(
                collider_data.name)
            object_properties: BSB_PG_ObjectProperties = collider_object.bsb_object_properties

            if (collider_object == None):
                continue

            collider_mesh = bmesh.new()
            collider_mesh.from_object(
                collider_object, depsgraph, cage=True, face_normals=False, vertex_normals=True
            )
            bmesh.ops.split_edges(collider_mesh, edges=collider_mesh.edges)

            tri_pack_objects.update(
                {
                    collider_data.name:
                    [
                        (loop.vert.co.x, loop.vert.co.y, loop.vert.co.z)
                        for triangle in collider_mesh.calc_loop_triangles()
                        for loop in triangle
                    ]
                }
            )

            collider_mesh.clear()
            collider_mesh.free()
# + (evaluated_mesh.vertices[vertex_index].normal * object_properties.collider_radius)
    return tri_pack_objects


def _BuildBatch(tri_coordinate_pack: list[tuple[float, float, float]]):
    shader: gpu.types.GPUShader = gpu.shader.from_builtin(
        "POLYLINE_UNIFORM_COLOR"
    )
    print(tri_coordinate_pack)
    batch = gpu_extras.batch.batch_for_shader(
        shader,
        "TRIS",
        {"pos": tri_coordinate_pack}
    )

    return shader, batch


def BSB_PrepareCollisionShapes(scene, depsgraph):

    object_tripack = _BuildVisualCollision(scene, depsgraph)

    tris = []
    for tripack_key, tripack_value in object_tripack.items():
        tris.extend(tripack_value)

    return _BuildBatch(tris)


def BSB_RenderCollisionShapes(context: bpy.types.Context):
    wm = context.window_manager
    shader: gpu.types.GPUShader = wm.bsb_collision_rendering["shader"]
    batch: gpu.types.GPUBatch = wm.bsb_collision_rendering["batch"]

    shader.uniform_float("viewportSize", gpu.state.viewport_get()[2:])
    shader.uniform_float("lineWidth", 2.5)
    shader.uniform_float("color", (1, 1, 0, 1))

    batch.draw(shader)


class BSB_OT_EnableCollisionDisplay(bpy.types.Operator):
    bl_label = ""
    bl_idname = "bsb.operator_enable_collision_display"

    bl_options = {"REGISTER", "UNDO"}

    draw_handler = None

    @classmethod
    def poll(self, context: bpy.types.Context):
        return True

    def terminate_modal(self, context):
        wm: bpy.types.WindowManager = context.window_manager

        try:
            bpy.types.SpaceView3D.draw_handler_remove(
                wm.bsb_collision_rendering["handler"],
                "WINDOW"
            )
            wm.bsb_collision_rendering["handler"] = None
        except:
            pass

        for area in context.screen.areas:
            area.tag_redraw()

        return {"FINISHED"}

    def modal(self, context: bpy.types.Context, event: bpy.types.Event):
        if (event.type == "ESC"):
            return self.terminate_modal(context)

        for area in context.screen.areas:
            area.tag_redraw()

        wm: bpy.types.WindowManager = context.window_manager
        wm.bsb_collision_rendering["shader"], wm.bsb_collision_rendering["batch"] = BSB_PrepareCollisionShapes(
            context.scene,
            context.evaluated_depsgraph_get()
        )

        return {"PASS_THROUGH"}

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        wm: bpy.types.WindowManager = context.window_manager

        if (wm.bsb_collision_rendering["handler"] is not None):
            return self.terminate_modal(context)

        else:

            BSB_synchronize_sandbox(context)

            wm.bsb_collision_rendering["shader"], wm.bsb_collision_rendering["batch"] = BSB_PrepareCollisionShapes(
                context.scene,
                context.evaluated_depsgraph_get()
            )

            args = tuple([context])
            wm.bsb_collision_rendering["handler"] = bpy.types.SpaceView3D.draw_handler_add(
                BSB_RenderCollisionShapes,
                args,
                "WINDOW",
                "POST_VIEW"
            )

            wm.modal_handler_add(self)
            return {"RUNNING_MODAL"}

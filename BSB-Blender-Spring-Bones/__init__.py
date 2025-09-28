
from .BSB_Properties import BSB_RegisterProperties, BSB_UnregisterProperties
from .modules.ALXAddonUpdater.ALXAddonUpdater.ALX_AddonUpdater import \
    Alx_Addon_Updater
from .modules.ALXModuleManager.ALXModuleManager.ALX_ModuleManager import \
    Alx_Module_Manager

bl_info = {
    "name": "BSB-Blender-Spring-Bones",
    "author": "Valerie Bosco, Artell[original dev]",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "Properties > Bones",
    "description": "Add a spring dynamic effect to a single/multiple bones",
    "category": "Animation"
}

module_manager = Alx_Module_Manager(
    path=__path__,
    globals=globals(),
    mute=True
)
addon_updater = Alx_Addon_Updater(
    path=__path__,
    bl_info=bl_info,
    engine="Github",
    engine_user_name="Valerie-Bosco",
    engine_repo_name="BSB-Blender-Spring-Bones",
    manual_download_website="https://github.com/Valerie-Bosco/BSB-Blender-Spring-Bones/releases/tag/main_branch_latest"
)


def register():
    module_manager.developer_register_modules()
    addon_updater.register_addon_updater(mute=True)

    BSB_RegisterProperties()

    # bpy.app.handlers.frame_change_post.append(BSB_FrameChangePost)


def unregister():
    module_manager.developer_unregister_modules()
    addon_updater.unregister_addon_updater()

    BSB_UnregisterProperties()
    #
    #

    # bpy.app.handlers.frame_change_post.remove(BSB_FrameChangePost)


if __name__ == "__main__":
    register()

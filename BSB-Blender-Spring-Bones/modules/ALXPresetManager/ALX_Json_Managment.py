import json
from pathlib import Path


def _verify_presets_module():

    presets_path = Path(__file__).parent.joinpath("presets")
    if (presets_path.exists() == False):
        presets_path.mkdir(parents=True, exist_ok=True)

    presets_definitions_path = presets_path.joinpath(
        "presets_definitions.json"
    )

    if (presets_definitions_path.exists() == False):
        presets_definitions_path.touch(exist_ok=True)

    if (presets_definitions_path.is_file()):
        pass


def write_property_value(type: type, property_path: str, property_value):
    """
    type: bpy.types.example

    property_path: .path_from_id("your_property")
        ie: object_properties_property_group.path_from_id(custom_string_variable_name)
        ie: object.path_from_id(custom_string_variable_name)
    """

    json.dump({
        f"{type}": {
            f"{property_path}": f"{property_value}"
        }},
        sort_keys=True
    )

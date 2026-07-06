"""
Folder generation utilities.
"""


def get_mesh_folder(topology: str, backhaul: str) -> str:
    """
    Return folder name for Mesh mode.
    """

    if topology == "DC":
        return f"01.1 Mesh_DC_{backhaul}"

    return f"02.1 Mesh_Star_{backhaul}"

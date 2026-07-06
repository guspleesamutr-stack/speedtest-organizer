"""
Folder generation utilities.
"""


def get_mesh_folder(topology, backhaul):
    """
    Return output folder name for Mesh mode.
    """

    if topology == "DC":
        return f"01.1 Mesh_DC_{backhaul}"

    return f"02.1 Mesh_Star_{backhaul}"

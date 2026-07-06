from core.constants import BACKHAULS


def get_mesh_folder(topology: str, backhaul: str) -> str:
    """
    Return folder name for Mesh mode.
    """

    backhaul_index = BACKHAULS.index(backhaul) + 1
    index_text = str(backhaul_index).zfill(2)

    if topology == "DC":
        return f"01_{index_text} Mesh_DC_{backhaul}"

    return f"02_{index_text} Mesh_Star_{backhaul}"

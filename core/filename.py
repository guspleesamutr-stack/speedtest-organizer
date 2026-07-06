"""
Filename generation utilities.
"""


def build_standalone_filename(
    distance,
    band,
    device,
    channel,
):
    filename = (
        f"SA_"
        f"{distance}_"
        f"{band}_"
        f"{device}"
    )

    if channel:
        filename += f"_CH{channel}"

    return filename

def build_mesh_wifi_filename(
    topology,
    backhaul,
    router,
    distance,
    band,
    device,
    channel,
):
    filename = (
        f"Mesh_"
        f"{topology}_"
        f"{backhaul}_"
        f"{router}_"
        f"{distance}_"
        f"{band}_"
        f"{device}"
    )

    if channel:
        filename += f"_CH{channel}"

    return filename

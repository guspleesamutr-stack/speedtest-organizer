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

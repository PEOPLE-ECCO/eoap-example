from dataclasses import dataclass

@dataclass
class Parameters:
    BANDS: list[str]
    TEMP_EXTENT: tuple[str, str]
    SPATIAL_EXTENT: dict[str, float]
    MAX_CLOUD_COVER: int


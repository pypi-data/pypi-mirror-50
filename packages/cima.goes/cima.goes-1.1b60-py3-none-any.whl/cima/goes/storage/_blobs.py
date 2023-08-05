from dataclasses import dataclass
from typing import Union
from google.cloud.storage.blob import Blob as GCSBlob

GoesBlob = Union[GCSBlob]


@dataclass
class BlobsGroup:
    start: str
    BLUE: GoesBlob = None
    RED: GoesBlob = None
    VEGGIE: GoesBlob = None
    CIRRUS: GoesBlob = None
    SNOW_ICE: GoesBlob = None
    CLOUD_PARTICLE_SIZE: GoesBlob = None
    SHORTWAVE_WINDOW: GoesBlob = None
    UPPER_LEVEL_TROPOSPHERIC_WATER_VAPOR: GoesBlob = None
    MID_LEVEL_TROPOSPHERIC_WATER_VAPOR: GoesBlob = None
    LOWER_LEVEL_WATER_VAPOR: GoesBlob = None
    CLOUD_TOP_PHASE: GoesBlob = None
    OZONE: GoesBlob = None
    CLEAN_LONGWAVE_WINDOW: GoesBlob = None
    IR_LONGWAVE_WINDOW: GoesBlob = None
    DIRTY_LONGWAVE_WINDOW: GoesBlob = None
    CO2_LONGWAVE_INFRARED: GoesBlob = None



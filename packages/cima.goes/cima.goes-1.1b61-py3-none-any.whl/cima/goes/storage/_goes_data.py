import abc
from typing import List
from cima.goes.storage._blobs import BlobsGroup, GoesBlob
from cima.goes import band
from netCDF4 import Dataset


class GoesData(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_grouped_blobs(self, year: int, day_of_year: int, hour: int, bands: List[band]) -> List[BlobsGroup]:
        pass

    @abc.abstractmethod
    def get_dataset(self, blob: GoesBlob) -> Dataset:
        pass

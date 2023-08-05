import os
import io
import netCDF4
from collections import namedtuple
from typing import List
import google.cloud.storage as gcs
from google.oauth2 import service_account
from cima.goes import file_pattern, path_prefix, slice_obs_start, product, mode
from cima.goes import band
from cima.goes.storage._file_systems import Storage, storage_type
from cima.goes.storage._blobs import BlobsGroup, GoesBlob
from cima.goes.storage._goes_data import GoesData


# Browse: https://console.cloud.google.com/storage/browser/gcp-public-data-goes-16
GOES_PUBLIC_BUCKET = 'gcp-public-data-goes-16'


class GCS(Storage, GoesData):
    '''
    Google Cloud Storage
    '''
    def __init__(self, credentials_as_dict: dict=None,
                 bucket: str=GOES_PUBLIC_BUCKET,
                 product: product=product.CMIPF, mode: mode=mode.M3,
                 credentials_filepath: str=None):
        self.stype = storage_type.GCS
        if credentials_as_dict is not None:
            self.set_credentials_dict(credentials_as_dict)
        else:
            self.credentials = None
            if credentials_filepath is not None:
                self.set_credentials(credentials_filepath)
        self.product = product
        self.mode = mode
        self.bucket = bucket

    #
    # Storage methods
    #
    async def list(self, path):
        return self.list_blobs(path)

    async def download_stream(self, filepath):
        return self.download_as_stream(filepath)

    async def mkdir(self, path):
        raise Exception('Not implemented: mkdir')

    async def upload_stream(self, data, filepath):
        raise Exception('Not implemented: upload_stream')

    #
    # GoesData methods
    #
    def get_dataset(self, blob: GoesBlob) -> netCDF4.Dataset:
        data = self.download_from_blob(blob)
        return netCDF4.Dataset("in_memory_file", mode='r', memory=data)

    def get_grouped_blobs(self, year: int, day_of_year: int, hour: int, bands: List[band]) -> List[BlobsGroup]:
        named_blobs = {}
        for band in bands:
            named_blobs[band.name] = self.band_blobs(year, day_of_year, hour, band)
        return self.group_blobs(named_blobs)

    #
    # GCS methods
    #
    def download_from_blob(self, blob):
        in_memory_file = io.BytesIO()
        blob.download_to_file(in_memory_file)
        in_memory_file.seek(0)
        return in_memory_file.read()

    def download_as_stream(self, filepath):
        client = gcs.Client(credentials=self.credentials, project='')
        bucket = client.get_bucket(self.bucket)
        blob = bucket.blob(filepath)
        return self.download_from_blob(blob)

    def download_dataset(self, filepath):
        data = self.download_as_stream(filepath)
        return netCDF4.Dataset("in_memory_file", mode='r', memory=data)

    def list_blobs(self, path: str):
        client = gcs.Client(credentials=self.credentials, project='')
        bucket = client.get_bucket(self.bucket)
        return bucket.list_blobs(prefix=path, delimiter='/')

    def band_blobs(self, year: int, day_of_year: int, hour: int, band: band):
      return self._list_blobs(
          path_prefix(year=year, day_of_year=day_of_year, hour=hour, product=self.product),
          [file_pattern(band=band.value, product=self.product, mode=self.mode)]
      )

    def group_blobs(self, named_blobs: dict) -> List[BlobsGroup]:
        blobs_by_start = {}
        names = [n for n, _ in named_blobs.items()]
        for name, blobs in named_blobs.items():
          for blob in blobs:
              key = blob.name[slice_obs_start(product=self.product)]
              if key not in blobs_by_start:
                  blobs_by_start[key] = {n: None for n in names}
              blobs_by_start[key][name] = blob
        result = []
        for k, v in blobs_by_start.items():
            result.append(BlobsGroup(**{'start':k, **{kk: vv for kk, vv in v.items()}}))
        return result

    def get_datasets(self, year: int, day_of_year: int, hour: int, bands: List[band]):
        blobs = self.get_blobs(year, day_of_year, hour, bands)
        Datasets = namedtuple('Datasets', ['start'] + [band.name for band in bands])
        for blob in blobs:
            data = {band.name: self.get_dataset(getattr(blob, band.name)) for band in bands}
            yield Datasets(start=blob.start, **data)

    def close_dataset(self, dataset):
        dataset.close()

    def close_datasets(self, datasets):
        for k in datasets._fields:
            if k != 'start':
                self.close_dataset(datasets._asdict()[k])

    def set_credentials(self, filepath: str):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = filepath

    def set_credentials_dict(self, credentials_as_dict: dict):
        self.credentials = service_account.Credentials.from_service_account_info(credentials_as_dict)

    def _list_blobs(self, path: str, gcs_patterns) -> List[GoesBlob]:
        blobs = self.list_blobs(path)
        result = []
        if gcs_patterns == None or len(gcs_patterns) == 0:
            for b in blobs:
                result.append(b)
        else:
            for b in blobs:
                match = True
                for pattern in gcs_patterns:
                    if not pattern in b.path:
                        match = False
                if match:
                    result.append(b)
        return result


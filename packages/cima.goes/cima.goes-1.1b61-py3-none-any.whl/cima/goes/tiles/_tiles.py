import io
import os
import json
import pyproj
from typing import Dict, List
from dataclasses import dataclass, asdict
from cima.goes import band
from cima.goes import GoesData, BlobsGroup, GoesBlob
from cima.goes.tasks import Task, run_concurrent
from cima.goes.storage._file_systems import goesdata_info, storage_info
from cima.goes.storage._factories import mount_goesdata, mount_store

try:
    import numpy as np
    # import cupy as cp
    cp = np
    asnumpy = cp.asnumpy
except:
    import numpy as np
    cp = np
    asnumpy = lambda x: x

FORTRAN_ORDER = 'F'


@dataclass
class Tile:
    lat_south: float
    lat_north: float
    lon_west: float
    lon_east: float

    x_min: int = None
    x_max: int = None
    y_min: int = None
    y_max: int = None


def get_tile_extent(tile, trim_excess=0) -> tuple:
    # (left, right, bottom, top)
    return (
        tile.lon_west + trim_excess,
        tile.lon_east - trim_excess,
        tile.lat_south + trim_excess,
        tile.lat_north - trim_excess
    )


@dataclass
class BandsTiles:
    BLUE: Dict[str, Tile] = None
    RED: Dict[str, Tile] = None
    VEGGIE: Dict[str, Tile] = None
    CIRRUS: Dict[str, Tile] = None
    SNOW_ICE: Dict[str, Tile] = None
    CLOUD_PARTICLE_SIZE: Dict[str, Tile] = None
    SHORTWAVE_WINDOW: Dict[str, Tile] = None
    UPPER_LEVEL_TROPOSPHERIC_WATER_VAPOR: Dict[str, Tile] = None
    MID_LEVEL_TROPOSPHERIC_WATER_VAPOR: Dict[str, Tile] = None
    LOWER_LEVEL_WATER_VAPOR: Dict[str, Tile] = None
    CLOUD_TOP_PHASE: Dict[str, Tile] = None
    OZONE: Dict[str, Tile] = None
    CLEAN_LONGWAVE_WINDOW: Dict[str, Tile] = None
    IR_LONGWAVE_WINDOW: Dict[str, Tile] = None
    DIRTY_LONGWAVE_WINDOW: Dict[str, Tile] = None
    CO2_LONGWAVE_INFRARED: Dict[str, Tile] = None


def generate_tiles(goes_info: goesdata_info,
                   bands: List[band],
                   lat_south: float,
                   lat_north: float,
                   lon_west: float,
                   lon_east: float,
                   lat_step: float,
                   lon_step: float,
                   lon_overlap: float,
                   lat_overlap: float,
                   workers=2,
                   ) -> BandsTiles:
    tasks = []
    for band in bands:
        tasks.append(
            Task(_get_indexed_tiles,
                 goes_info,
                 bands, band,
                 lat_south=lat_south, lat_north=lat_north,
                 lon_west=lon_west, lon_east=lon_east,
                 lat_step=lat_step, lon_step=lon_step,
                 lat_overlap=lat_overlap, lon_overlap=lon_overlap
            ))
    workers = min(workers, len(tasks))
    responses = run_concurrent(tasks, workers=workers)
    bands_tiles: BandsTiles = BandsTiles()
    for index, band in enumerate(bands):
        setattr(bands_tiles, responses[index][0], responses[index][1])
    return bands_tiles


def _get_indexed_tiles(goes_info: goesdata_info, bands: List[band], band: band, **kwargs):
    goesdata: GoesData = mount_goesdata(goes_info)
    blobs: List[BlobsGroup] = goesdata.get_grouped_blobs(2018, 360, 12, bands)
    dataset = goesdata.get_dataset(getattr(blobs[0], band.name))
    try:
        tiles = _get_tiles_one_band(**kwargs)
        tiles = _add_indexes_for_dataset(dataset, tiles)
        return (band.name, tiles)
    finally:
        dataset.close()


def save_tiles(store_info: storage_info, filepath: str, tiles: BandsTiles):
    data = bytes(json.dumps(asdict(tiles), indent=2), 'utf-8')
    in_memory_file = io.BytesIO()
    in_memory_file.write(data)
    in_memory_file.seek(0)
    store = mount_store(store_info)
    store.upload_stream(in_memory_file, filepath)


def load_tiles(store_info: storage_info, filepath) -> BandsTiles:
    store = mount_store(store_info)
    data = store.download_stream(filepath)
    tiles_dict = json.loads(data)
    return get_tiles_from_dict(tiles_dict)


def get_tiles_from_dict(tiles_dict) -> BandsTiles:
    bands_tiles: BandsTiles = BandsTiles()
    for band, v in tiles_dict.items():
        if v is not None:
            setattr(bands_tiles, band, {})
            for tile_number, tile_data in v.items():
                getattr(bands_tiles, band)[tile_number] = Tile(**tile_data)
    return bands_tiles


def get_lats_lons(dataset, tile: Tile = None):
    sat_height = dataset['goes_imager_projection'].perspective_point_height
    sat_lon = dataset['goes_imager_projection'].longitude_of_projection_origin
    sat_sweep = dataset['goes_imager_projection'].sweep_angle_axis
    projection = pyproj.Proj(proj='geos', h=sat_height, lon_0=sat_lon, sweep=sat_sweep)
    if tile is None:
        x = dataset['x'][:] * sat_height
        y = dataset['y'][:] * sat_height
    else:
        x = dataset['x'][tile.x_min: tile.x_max] * sat_height
        y = dataset['y'][tile.y_min: tile.y_max] * sat_height
    XX, YY = cp.meshgrid(cp.array(x), cp.array(y))
    lons, lats = projection(asnumpy(XX), asnumpy(YY), inverse=True)
    return cp.array(lats), cp.array(lons)


def _get_tiles_one_band(lat_south: float, lat_north: float,
                        lon_west: float, lon_east: float,
                        lat_step: float, lon_step: float,
                        lat_overlap: float, lon_overlap: float):
    """
    >>> _get_tiles_one_band(lat_south=-45, lat_north=-40, lon_west=-75, lon_east=-70, lat_step=5, lon_step=5, lon_overlap=1, lat_overlap=1)
    {'0': Tile(lat_south=-46.0, lat_north=-39.0, lon_west=-76.0, lon_east=-69.0, x_min=None, x_max=None, y_min=None, y_max=None)}
    >>> _get_tiles_one_band(lat_south=-43, lat_north=-33, lon_west=-75, lon_east=-70, lat_step=10, lon_step=2.5, lon_overlap=1, lat_overlap=1)
    {'0': Tile(lat_south=-44.0, lat_north=-32.0, lon_west=-76.0, lon_east=-71.5, x_min=None, x_max=None, y_min=None, y_max=None), '1': Tile(lat_south=-44.0, lat_north=-32.0, lon_west=-73.5, lon_east=-69.0, x_min=None, x_max=None, y_min=None, y_max=None)}
    """
    tiles = {}
    lats = [x for x in cp.arange(lat_south, lat_north, lat_step)]
    lons = [x for x in cp.arange(lon_west, lon_east, lon_step)]
    tiles_coordinates = [(lat, lat + lat_step, lon, lon + lon_step, ) for lat in lats for lon in lons]
    for index, lats_lons in enumerate(tiles_coordinates):
        tiles[str(index)] = Tile(
            lat_south = float(lats_lons[0] - lat_overlap),
            lat_north = float(lats_lons[1] + lat_overlap),
            lon_west = float(lats_lons[2] - lon_overlap),
            lon_east = float(lats_lons[3] + lon_overlap))
    return tiles


def _add_indexes_for_dataset(dataset, tiles):
    major_order = FORTRAN_ORDER
    lats, lons = get_lats_lons(dataset)
    _add_indexes(tiles, lats, lons, major_order)
    return tiles


def _nearest_indexes(lat, lon, lats, lons, major_order):
    distance = (lat - lats) * (lat - lats) + (lon - lons) * (lon - lons)
    return cp.unravel_index(cp.argmin(distance), lats.shape, major_order)

def _find_indexes(tile: Tile, lats, lons, major_order):
    x1, y1 = _nearest_indexes(tile.lat_north, tile.lon_west, lats, lons, major_order)
    x2, y2 = _nearest_indexes(tile.lat_north, tile.lon_east, lats, lons, major_order)
    x3, y3 = _nearest_indexes(tile.lat_south, tile.lon_west, lats, lons, major_order)
    x4, y4 = _nearest_indexes(tile.lat_south, tile.lon_east, lats, lons, major_order)

    tile.x_min = int(min(x1, x2, x3, x4))
    tile.x_max = int(max(x1, x2, x3, x4))
    tile.y_min = int(min(y1, y2, y3, y4))
    tile.y_max = int(max(y1, y2, y3, y4))


def _add_indexes(tiles, lats, lons, order):
    for index, tile in tiles.items():
        _find_indexes(tile, lats, lons, order)

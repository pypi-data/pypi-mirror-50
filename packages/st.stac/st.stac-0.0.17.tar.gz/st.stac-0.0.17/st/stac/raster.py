import os
from typing import List

from epl.protobuf import stac_pb2

DEFAULT_RGB = [stac_pb2.Eo.RED, stac_pb2.Eo.GREEN, stac_pb2.Eo.BLUE]
RASTER_TYPES = [stac_pb2.CO_GEOTIFF, stac_pb2.GEOTIFF, stac_pb2.MRF]


def get_asset(stac_item: stac_pb2.StacItem,
              cloud_platform: stac_pb2.CloudPlatform = stac_pb2.UNKNOWN_CLOUD_PLATFORM,
              band: stac_pb2.Eo.Band = stac_pb2.Eo.UNKNOWN_BAND,
              asset_types: List = None,
              strict=False,
              asset_basename: str = "") -> stac_pb2.Asset:
    """
    get an asset protobuf object(pb) from a stac item pb.
    :param stac_item: stac item whose assets we want to search by parameters
    :param cloud_platform: only return assets that are hosted on the cloud platform described in the cloud_platform field of the item. default grabs the first asset that meets all the other parameters.
    :param band: if the data has electro optical spectrum data, define the band you want to retrieve. if the data is not electro optical then don't define this parameter (defaults to UNKNOWN_BAND)
    :param asset_types: a list of asset_types to seach. if not defined then it is assumed to search all asset types
    :param strict: set to True means throw exception if nothing is found. otherwise return None
    :param asset_basename: only return asset if the basename of the object path matches this value
    :return: asset pb object
    """
    if asset_types is None:
        asset_types = [stac_pb2.AssetType.Value(asset_type_str) for asset_type_str in stac_pb2.AssetType.keys()]

    for asset_type in asset_types:
        for key in stac_item.assets:
            asset = stac_item.assets[key]
            if asset.asset_type != asset_type:
                continue
            if asset.eo_bands == band:
                if asset.cloud_platform == cloud_platform or cloud_platform == stac_pb2.UNKNOWN_CLOUD_PLATFORM:
                    if asset_basename and not _asset_has_filename(asset=asset, asset_basename=asset_basename):
                        continue
                    return asset

    if strict:
        raise ValueError("asset not found")
    return None


def _asset_has_filename(asset: stac_pb2.Asset, asset_basename):
    if os.path.basename(asset.object_path).lower() == os.path.basename(asset_basename).lower():
        return True
    return False


def get_assets(stac_item: stac_pb2.StacItem,
               cloud_platform: stac_pb2.CloudPlatform,
               bands: List = None,
               asset_types: List = None,
               strict=False) -> List:
    if bands is None:
        bands = DEFAULT_RGB

    if asset_types is None:
        asset_types = RASTER_TYPES

    if cloud_platform is None:
        cloud_platform = stac_pb2.UNKNOWN_CLOUD_PLATFORM

    assets = []
    for band in bands:
        if band == stac_pb2.Eo.RGB or band == stac_pb2.Eo.RGBIR:
            assets.extend(get_assets(stac_item=stac_item, bands=DEFAULT_RGB, cloud_platform=cloud_platform,
                                     asset_types=asset_types, strict=strict))
            if band == stac_pb2.Eo.RGBIR:
                assets.append(get_asset(stac_item=stac_item, band=stac_pb2.Eo.NIR, cloud_platform=cloud_platform,
                                        asset_types=asset_types, strict=strict))
        else:
            assets.append(
                get_asset(stac_item=stac_item,
                          band=band,
                          cloud_platform=cloud_platform,
                          asset_types=asset_types,
                          strict=strict))

    return assets


def has_asset_type(stac_item: stac_pb2.StacItem,
                   asset_type: stac_pb2.AssetType):
    for key in stac_item.assets:
        asset = stac_item.assets[key]
        if asset.asset_type == asset_type:
            return True
    return False


def has_asset(stac_item: stac_pb2.StacItem,
              asset: stac_pb2.Asset):
    if not has_asset_type(stac_item=stac_item, asset_type=asset.asset_type):
        return False
    for key in stac_item.assets:
        test_asset = stac_item.assets[key]
        # TODO should iterate over test_asset.DESCRIPTOR.fields, as in this example:
        #  https://stackoverflow.com/a/29150312/445372
        # for now we assume href makes for uniqueness of an asset
        if asset.asset_type == test_asset.asset_type and asset.href == test_asset.href:
            return True
    return False


def get_uri(asset: stac_pb2.Asset, b_vsi_uri=True, prefix: str = "") -> str:
    """
    construct the uri for the resource in the asset.
    :param asset: 
    :param b_vsi_uri:
    :param prefix:
    :return:
    """

    if not asset.bucket or not asset.object_path:
        if not b_vsi_uri:
            raise FileNotFoundError("The bucket ref is not AWS or Google:\nhref : {0}".format(asset.href))
        return '/vsicurl_streaming/{}'.format(asset.href)
    elif not prefix:
        prefix = "{0}://"
        if b_vsi_uri:
            prefix = "/vsi{0}_streaming"

        if asset.cloud_platform == stac_pb2.GCP:
            prefix = prefix.format("gs")
        elif asset.cloud_platform == stac_pb2.AWS:
            prefix = prefix.format("s3")
        else:
            raise ValueError("The only current cloud platforms are GCP and AWS. This asset doesn't have the "
                             "'cloud_platform' field defined")

    return "{0}/{1}/{2}".format(prefix, asset.bucket, asset.object_path)

import os

from aa_utils import data_utils, feature_utils, file_utils, geometry_utils, map_utils
from aa_utils.raster_utils import Raster
from qgis.core import *


def get_rasters(root):
    prj_ext = ".qgz"
    lyr_ext = ".qlr"
    result = []

    project_files = file_utils.find_files_by_extension(root, prj_ext) + file_utils.find_files_by_extension(root, ".qgs")
    for project_file in project_files:
        project = map_utils.load_project(project_file)
        layers = map_utils.get_layers_from_project(project)
        raster_files = map_utils.get_raster_layer_sources(layers)
        for raster in raster_files:
            if os.path.isfile(raster):
                result.append(raster)
            else:
                print(f"Warn: {raster} is not a valid source")

    layer_files = file_utils.find_files_by_extension(root, lyr_ext)
    for layer_file in layer_files:
        layer_list = map_utils.read_layer_file(layer_file)
        raster_files = map_utils.get_raster_layer_sources(layer_list)
        for raster in raster_files:
            result.append(raster)

    distinct_result = set(result)
    print(f"{len(distinct_result)} distinct raster layers found in {root}")

    return list(distinct_result)


# Supply path to qgis install location
QgsApplication.setPrefixPath('C:/PROGRA~1/QGIS32~1.4/apps/qgis-ltr', True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], False)

# Load providers
qgs.initQgis()

gpkg = data_utils.GeoPackage(r"Y:\AA\aagisdat\QGIS\Edit_Technik\Raster.gpkg")
lyr = gpkg.layers[0]

for rf in get_rasters(r"Y:\AA"):
    try:
        if rf.startswith("Q:"):
            print(f"Ignore raster from Q drive: {rf}")
            continue
        r = Raster(rf)
        if r.extent is None:
            print(f"Warn: Could not get extent for {rf}")
            continue
        geom = geometry_utils.polygon_from_extent(r.extent[0], r.extent[1], r.extent[2], r.extent[3])
        feat = feature_utils.new_feature()
        feat.setFields(lyr.fields())
        feature_utils.set_geometry(feat, geom)
        feat.setAttribute('RasterPfad', rf)
        feat.setAttribute('BandCount', r.band_count)
        feat.setAttribute('SpatialReference', r.spatial_reference)
        print(f"Store feature from {rf}")
        lyr.dataProvider().addFeature(feat)
    except Exception as e:
        print(f"Unexpected error for {rf}: {e}")
        continue

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()

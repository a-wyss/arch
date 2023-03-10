from typing import List

import qgis.utils
from qgis.core import QgsMapLayer, QgsFeature, QgsProject, QgsRasterLayer, QgsLayerDefinition


def get_selected_layer():
    """
    Returns a pointer to the active layer (layer selected in the legend)
    :rtype: QgsMapLayer
    """
    return qgis.utils.iface.activeLayer()


def get_selected_features():
    """
    Returns a copy of the user-selected features in the active layer.
    :rtype: List[QgsFeature]
    """
    lyr = get_selected_layer()
    return lyr.selectedFeatures()


def load_project(project_path):
    """
    Get project instance from an existing QGIS project file
    :param str project_path: path to QGIS project
    :return: the project instance

    """
    project = QgsProject()
    project.read(project_path)
    print(f"Successfully opened {project_path}")

    return project


def create_project():
    return QgsProject()


def read_layer_file(qlr_file):
    return QgsLayerDefinition().loadLayerDefinitionLayers(qlr_file)


def get_layers_from_project(project):
    """
    :param QgsProject project:
    :return: List with all layers within project
    :rtype: List[QgsMapLayer]
    """
    return project.mapLayers().values()


def get_raster_layer_sources(layers):
    """
    :param List[QgsMapLayer] layers:
    :return: List with all raster layers within project
    :rtype: List[str]
    """
    result = []
    for layer in layers:
        if isinstance(layer, QgsRasterLayer):
            result.append(layer.dataProvider().dataSourceUri())
    print(f"Found {len(result)} raster layer in current project")

    return result


"""
-------------------------------------
Action code (use in layer properties)
-------------------------------------
- load raster from source (RasterPfad is the field name where the absolute path is stored):
qgis.utils.iface.addRasterLayer('[% "RasterPfad" %]', os.path.basename(os.path.splitext('[% "RasterPfad" %]')[0]))

"""
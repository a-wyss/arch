from qgis.core import QgsFeature, QgsGeometry


def new_feature():
    return QgsFeature()


def set_geometry(feature, geometry):
    """
    Set the geometry to the given feature. If feature is None a new feature is created
    :param QgsFeature feature: the feature to which the geometry is to be set
    :param QgsGeometry geometry: the geometry (point, line, polygon, ...)
    """
    if not feature:
        feature = new_feature()
    feature.setGeometry(geometry)

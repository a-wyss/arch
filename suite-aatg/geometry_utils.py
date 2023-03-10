from qgis.core import QgsPoint, QgsGeometry, QgsRectangle


def create_point(x, y, z=None):
    """
    Create a point object from given coordinates.\n
    :param float x: the x / east coordinate of the point
    :param float y: the y / north coordinate of the point
    :param float z: optional -> the height of the point
    :return: QgsPoint
    """
    return QgsPoint(x, y, z) if z else QgsPoint(x, y)


def get_nearest_point(src_geometry, target_geometry):
    """
    :param QgsGeometry src_geometry:
    :param QgsGeometry target_geometry:
    :return: Returns the nearest point on src_geometry to target_geometry
    :rtype: QgsGeometry
    """
    return src_geometry.nearestPoint(target_geometry)


def polygon_from_extent(x_min, y_min, x_max, y_max):
    """
    Get geometry from extent
    :param float x_min: lower left coordinate
    :param float y_min: lower left coordinate
    :param float x_max: upper right coordinate
    :param float y_max: upper right coordinate
    :return: The extent as geometry
    """
    rect = QgsRectangle(x_min, y_min, x_max, y_max)
    return QgsGeometry.fromRect(rect)


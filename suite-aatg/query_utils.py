from typing import List

from qgis.core import QgsMapLayer, QgsFeature


def get_difference(layer1, layer2, field1, field2):
    """
    Get the difference between features of two layers for a given attribute.
    :param QgsMapLayer layer1:
    :param QgsMapLayer layer2:
    :param str field1: The field name to query the attributes from layer1
    :param str field2: The field name to query the attributes from layer2
    :return: A list of features/attributes which are in layer1 but not in layer2
    :rtype: List[QgsFeature]
    """
    features1 = [f[field1] for f in layer1.getFeatures()]
    features2 = [f[field2] for f in layer2.getFeatures()]

    return [f for f in features1 if f not in features2]

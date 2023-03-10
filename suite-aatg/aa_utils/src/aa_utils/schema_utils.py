import qgis.PyQt.QtCore
from qgis.core import QgsVectorLayer, QgsField, QgsVectorDataProvider, QgsDefaultValue


def add_field(layer, field_definition, default_value, update_default=False):
    """
    Add field to vector layer.
    :param QgsVectorLayer layer: input layer
    :param QgsField field_definition: the definition of the field
    :param str default_value:
    :param bool update_default:
    :return:
    """
    caps = layer.dataProvider().capabilities()
    if caps & QgsVectorDataProvider.AddAttributes:
        layer.dataProvider().addAttributes([field_definition])
        if default_value:
            layer.setDefaultValueDefinition(layer.fields().indexFromName(field_definition.name()),
                                            QgsDefaultValue(default_value, update_default))
        layer.updateFields()
    else:
        print(f'Not able to update {layer.name()}')


def define_string_field(field_name, length):
    return QgsField(field_name, qgis.PyQt.QtCore.QVariant.String, '', length)


def define_datetime_field(field_name):
    return QgsField(field_name, qgis.PyQt.QtCore.QVariant.DateTime)

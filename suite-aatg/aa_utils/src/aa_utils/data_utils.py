from osgeo import ogr
from qgis.core import QgsVectorLayer


class GeoPackage(object):
    def __init__(self, path):
        self.path = path
        self.__gpkg = ogr.Open(self.path)

    @property
    def layers(self):
        return [QgsVectorLayer(self.path, lyr.GetName(), 'ogr') for lyr in self.__gpkg]
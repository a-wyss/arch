from osgeo import gdal
from aa_utils.constants import RasterBandDataType


class Raster(object):
    def __init__(self, in_file):
        self.__file = in_file
        print(f"Reading {self.__file}")
        self.raster = gdal.Open(self.__file)

        self.__bands = {}

    @property
    def is_valid(self):
        if not self.raster:
            raise ValueError(f"{self.__file} is unsupported raster file")

        return True

    @property
    def extent(self):
        """
        :return: the extent of the raster: xMin, yMin, xMax, yMax
        """
        try:
            if self.is_valid:
                ulx, xres, xskew, uly, yskew, yres = self.raster.GetGeoTransform()

                lrx = ulx + (self.raster.RasterXSize * xres)
                lry = uly + (self.raster.RasterYSize * yres)

                return float(ulx), float(lry), float(lrx), float(uly)
        except ValueError as ve:
            print(f"Error: {ve}")
            return None

    @property
    def spatial_reference(self):
        try:
            return self.raster.GetSpatialRef().GetName()
        except Exception as e:
            print(f"Error: {e}")
            return None

    @property
    def band_count(self):
        return self.raster.RasterCount

    def get_band(self, band_idx=1):
        if band_idx not in self.__bands.keys():
            band = RasterBand(self.raster.GetRasterBand(band_idx))
            self.__bands.update({band_idx: band})

        return self.__bands[band_idx]


class RasterBand(object):
    def __init__(self, band):
        self.__band = band
        self.__band.GetStatistics(1, 1)

    @property
    def max(self):
        return self.__band.GetMaximum()

    @property
    def min(self):
        return self.__band.GetMinimum()
    
    @property
    def data_type(self):
        return RasterBandDataType(self.__band.DataType).name

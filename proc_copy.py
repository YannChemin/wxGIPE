# -*- coding: utf-8 -*-
from osgeo import gdal
from osgeo.gdalconst import *

import numpy
from osgeo import gdalnumeric

import sys

# =============================================================================
def ParseType(type):
    if type == 'Byte':
	return GDT_Byte
    elif type == 'Int16':
	return GDT_Int16
    elif type == 'UInt16':
	return GDT_UInt16
    elif type == 'Int32':
	return GDT_Int32
    elif type == 'UInt32':
	return GDT_UInt32
    elif type == 'Float32':
	return GDT_Float32
    elif type == 'Float64':
	return GDT_Float64
    elif type == 'CInt16':
	return GDT_CInt16
    elif type == 'CInt32':
	return GDT_CInt32
    elif type == 'CFloat32':
	return GDT_CFloat32
    elif type == 'CFloat64':
	return GDT_CFloat64
    else:
	return GDT_Byte
# =============================================================================

inNoData = None
outNoData = None
infile = None
outfile = None
format = 'GTiff'
type = GDT_Float32

# Parse command line arguments.
inNoData = self.infile
outNoData = self.outfile
format = sys.argv[i]
type = ParseType(sys.argv[i])

    elif infile is None:
	infile = arg

    elif outfile is None:
	outfile = arg

    else:
	Usage()

    i = i + 1

if infile is None:
    Usage()
if  outfile is None:
    Usage()
if inNoData is None:
    Usage()
if outNoData is None:
    Usage()

indataset = gdal.Open( infile, GA_ReadOnly )

out_driver = gdal.GetDriverByName(format)
outdataset = out_driver.Create(outfile, indataset.RasterXSize, indataset.RasterYSize, indataset.RasterCount, type)

for iBand in range(1, indataset.RasterCount + 1):
    inband = indataset.GetRasterBand(iBand)
    outband = outdataset.GetRasterBand(iBand)

    for i in range(inband.YSize - 1, -1, -1):
	scanline = inband.ReadAsArray(0, i, inband.XSize, 1, inband.XSize, 1)
        scanline = gdalnumeric.choose( gdalnumeric.equal( scanline, inNoData),
                                       (scanline, outNoData) )
	outband.WriteArray(scanline, 0, i)


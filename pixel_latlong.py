#!/usr/bin/env python

import gdal
from gdalconst import *
import osr
import sys

# =============================================================================
def Usage():
    print
    print 'Read coordinate system and geotransformation matrix from input'
    print 'file and print latitude/longitude coordinates for the specified'
    print 'pixel.'
    print
    print 'Usage: tolatlong.py pixel line infile'
    print
    sys.exit( 1 )

# =============================================================================

infile = None
pixel = None
line = None

# =============================================================================
# Parse command line arguments.
# =============================================================================
i = 1
while i < len(sys.argv):
    arg = sys.argv[i]

    if pixel is None:
	pixel = float(arg)

    elif line is None:
	line = float(arg)

    elif infile is None:
	infile = arg

    else:
	Usage()

    i = i + 1

if infile is None:
    Usage()
if pixel is None:
    Usage()
if line is None:
    Usage()

indataset = gdal.Open( infile, GA_ReadOnly )

geomatrix = indataset.GetGeoTransform()
X = geomatrix[0] + geomatrix[1] * pixel + geomatrix[2] * line
Y = geomatrix[3] + geomatrix[4] * pixel + geomatrix[5] * line

srs = osr.SpatialReference()
srs.ImportFromWkt(indataset.GetProjection())

srsLatLong = srs.CloneGeogCS()
ct = osr.CoordinateTransformation(srs, srsLatLong)
(long, lat, height) = ct.TransformPoint(X, Y)

print 'pixel: %g, line: %g' % (pixel, line)
print 'latitude: %g, longitude: %g (in degrees)' % (long, lat)
#!/bin/sh

# 2005, Markus Neteler
# warp MODIS HDF to Erdas/Img - LatLong/WGS84

PROG="$0"

if [ $# -lt 1 -o "$1" = "-h" -o "$1" = "--help" -o "$1" = "-help" ] ; then
 echo "Script to warp all layers of MODIS HDF to Erdas/Img - LatLong/WGS84"
 echo "Usage:"
 echo "      $PROG M[OD|MYD]blabla.hdf"
 exit 1
fi

FILE=$1
HDFlayerNAMES="`gdalinfo $FILE | grep SUBDATASET_ | grep _NAME | cut -d'=' -f2`"

#aarg! NDVI/EVI MOD13 contains spaces:
HDFlayerNAMES_NOSPACES="`gdalinfo $FILE | grep SUBDATASET_ | grep _NAME | cut -d'=' -f2 | tr -s ' ' '|'`"

#MODIS does not use the "Normal Sphere (r=6370997)"!!!
# MODIS sphere, radius of 6371007.181
# http://edcdaac.usgs.gov/landdaac/tools/mrtswath/info/ReleaseNotes.pdf
#
# WGS 84
# <4326> +proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs  <>

# cs2cs -le
SPHERE="+ellps=sphere"

#loop over all layers:
for i in ${HDFlayerNAMES_NOSPACES} ; do
        #transform back:
        INPUT="`echo ${i} | tr -s '|' ' '`"
	NEWNAME="`echo ${i} | cut -d':' -f4,5 | tr ':' '_' | tr -s '|' '_'`"
	# apply GCPs
	gdalwarp -of HFA -t_srs "+proj=latlong $SPHERE" "${INPUT}" $NEWNAME.tmp.img
	# fix the LatLong reference cut to fit into world map (ulx uly lrx lry):
	# -projwin -180 90 180 -90
	# not desired for NDVI etc
	gdal_translate -of HFA -a_srs "EPSG:4326" \
	    -co COMPRESS=YES \
            $NEWNAME.tmp.img $NEWNAME.wgs84_LL.img
	rm -f $NEWNAME.tmp.img
done


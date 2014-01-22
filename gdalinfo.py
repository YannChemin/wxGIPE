#!/usr/bin/python

try:
	from osgeo import gdal
	from osgeo import _gdal
except:
	import gdal
	import _gdal

from osgeo.gdalconst import *
#from gdalalg import *

try:
	from osgeo import ogr
except:
	import ogr
try:
	from osgeo import osr
except:
	import osr

import sys
#include "gdal.h"
#include "gdal_alg.h"
#include "ogr_srs_api.h"
#include "cpl_string.h"
#include "cpl_conv.h"
#include "cpl_multiproc.h"

"""CPL_CVSID("$Id: gdalinfo.c 12555 2007-10-27 12:58:01Z rouault $");

static int 
GDALInfoReportCorner( GDALDatasetH hDataset, 
                      OGRCoordinateTransformationH hTransform,
                      const char * corner_name,
                      double x, double y );
"""
#class gdalinfo(argc, argv[]):
"""/******************************************************************************
 * gdalinfo.py 
 *
 * Project:  GDAL Utilities
 * Purpose:  Commandline application to list info about a file.
 * Author:   
 *	Original C code: Frank Warmerdam, warmerdam@pobox.com
 *	Copyright (c) 1998, Frank Warmerdam
 *
 *	Translation in python: Yann Chemin, yann.chemin@gmail.com
 * ****************************************************************************
 * Copyright (c) 2008, Yann Chemin
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 ****************************************************************************/
"""


def Usage():
	"""
	/************************************************************************/
	/*                               Usage()                                */
	/************************************************************************/
	"""
	print 'Usage: gdalinfo 	[--help-general] [-mm] [-stats] [-nogcp] [-nomd]'
	print '              	[-noct] [-checksum] [-mdd domain]* datasetname'

if __name__ == '__main__':
	
	gdal.AllRegister()
	argv = gdal.GeneralCmdLineProcessor( sys.argv )
	if argv is None:
		sys.exit( 0 )
	
	#GDALDatasetH        hDataset;
	#hDataset	= _gdal._GDALDatasetH
	#GDALRasterBandH     hBand;
	#hBand 		= gdal.GDALRasterBandH()
	#int                 i, iBand;
	#i 		= 0
	#iBand 		= 0
	#double              adfGeoTransform[6];
#	adfGeoTransform	= _gdal.ptrcreate('double',0,6)
#	for i in range(6):
#		_gdal.ptrset(adfGeoTransform,0.0,i)
	#GDALDriverH         hDriver;
	#hDriver		= gdal.GDALDriverH()
	#char                **papszMetadata;
	papszMetadata 	= []
	#int                 bComputeMinMax = False, bSample = False;
	bComputeMinMax 	= False
	bSample 	= False
	#int                 bShowGCPs = True, bShowMetadata = True ;
	bShowGCPs 	= True 
	bShowMetadata 	= True
	#int                 bStats = False, bApproxStats = True, iMDD;
	bStats 		= False
	bApproxStats 	= True 
	iMDD 		= 0
	#int                 bShowColorTable = True, bComputeChecksum = False;
	bShowColorTable = True
	bComputeChecksum = False
	#const char          *pszFilename = NULL;
	pszFilename 	= None
	#char              **papszExtraMDDomains = NULL, **papszFileList;
	papszExtraMDDomains = []
	#papszFileList 	= []
	#const char  *pszProjection = NULL;
	pszProjection	= None
	#OGRCoordinateTransformationH hTransform = NULL;
	#hTransform 	= gdal.OGRCoordinateTransformationH()

#00224 typedef struct
#00225 {
#00227     char        *pszId; 
#00228 
#00230     char        *pszInfo;
#00231 
#00233     double      dfGCPPixel;
#00235     double      dfGCPLine;
#00236 
#00238     double      dfGCPX;
#00239 
#00241     double      dfGCPY;
#00242 
#00244     double      dfGCPZ;
#00245 } GDAL_GCP;

#/* -------------------------------------------------------------------- */
#/*      Parse arguments.                                                */
#/* -------------------------------------------------------------------- */
	# Parse command line arguments.
	i = 1
	while i < len(argv):
		arg = argv[i]
	
		if arg == '-mm':
			bComputeMinMax = True
			print 'bComputeMinMax: ',bComputeMinMax
	
		elif arg == '-stats':
			bStats = True
			bApproxStats = False
			print 'bStats: ',bStats
			print 'bApproxStats: ',bApproxStats
	
		elif arg == '-approx_stats':
			bStats = True
			bApproxStats = True
			print 'bStats: ',bStats
			print 'bApproxStats: ',bApproxStats
	
		elif arg ==  '-sample':
			bSample = True
			print 'bSample: ',bSample
	
		elif arg ==  '-checksum':
			bComputeChecksum = True
			print 'bComputeChecksum: ',bComputeChecksum
	
		elif arg ==  '-nogcp':
			bShowGCPs = False
			print 'bShowGCPs: ',bShowGCPs
	
		elif arg ==  '-nomd':
			bShowMetadata = False
			print 'bShowMetadata: ',bShowMetadata
	
		elif arg ==  '-noct':
			bShowColorTable = False
			print 'bShowColorTable: ',bShowColorTable
	
		elif arg ==  '-mdd':
			i = i + 1
			papszExtraMDDomains.Append( argv[i] )
			print 'papszExtraMDDomains: ',papszExtraMDDomains
	
		elif arg[:1] == '-':
			print 'Unrecognised command option: ', arg
			Usage()
			sys.exit( 1 )
	
		elif pszFilename == None:
			pszFilename = argv[i]
			#print 'pszFilename: ',pszFilename

		else: pass
		    #Usage()
		i = i+1

	if pszFilename == None:
		Usage()

#/* -------------------------------------------------------------------- */
#/*      Open dataset.                                                   */
#/* -------------------------------------------------------------------- */
	hDataset = _gdal.Open( pszFilename, gdal.GA_ReadOnly )
	if hDataset == None:
		print 'gdalinfo failed - unable to open', pszFilename
		sys.exit( 1 )
	    
#/* -------------------------------------------------------------------- */
#/*      Report general info.                                            */
#/* -------------------------------------------------------------------- */
	hDriver = _gdal.Dataset_GetDriver( hDataset )
	print "Driver: ", _gdal.Driver_ShortName_get( hDriver ), " ", _gdal.Driver_LongName_get( hDriver )
	papszFileList = _gdal.GetFileList( hDataset )
	if _gdal.CSLCount(papszFileList) == 0:
		print 'Files: none associated'
	else:
		print 'Files: ', _gdal.papszFileList[0]
		i = 1
		while papszFileList[i] != None:
			print papszFileList[i]
			i = i+1
	_gdal.CSLDestroy( papszFileList )
	print "Size is ", _gdal.GetRasterXSize( hDataset )," ",_gdal.GDALGetRasterYSize( hDataset )
    
#/* -------------------------------------------------------------------- */
#/*      Report projection.                                              */
#/* -------------------------------------------------------------------- */
#	if _gdal.GDALGetProjectionRef( hDataset ) != None :
#		#OGRSpatialReferenceH  hSRS;
#		#char                  *pszProjection;
#		pszProjection = _gdal.GDALGetProjectionRef( hDataset )
#		#print 'pszProjection = ', pszProjection
#		hSRS = _gdal.OSRNewSpatialReference( '' )
#		#print 'hSRS = ', hSRS
#		if _gdal.OSRImportFromWkt( hSRS, pszProjection ) == '' :
#			# == CE_None
#			#char        *pszPrettyWkt = NULL;
#			pszPrettyWkt = None
#			_gdal.OSRExportToPrettyWkt( hSRS, pszPrettyWkt, False )
##			print 'Coordinate System is: ', pszPrettyWkt
#			_gdal.CPLFree( pszPrettyWkt )
#		else:
#			print 'Coord. System: ', _gdal.GDALGetProjectionRef( hDataset )
#		_gdal.OSRDestroySpatialReference( hSRS )

#/* -------------------------------------------------------------------- */
#/*      Report Geotransform.                                            */
#/* -------------------------------------------------------------------- */
#	if _gdal.GDALGetGeoTransform( hDataset, adfGeoTransform ) == '' :
#		# == CE_None
##		if adfGeoTransform[2] == 0.0 and adfGeoTransform[4] == 0.0:
#			print 'Origin = ',adfGeoTransform[0], adfGeoTransform[3]
#			print 'Pixel Size = ',adfGeoTransform[1], adfGeoTransform[5]
#		else:
#			print 'GeoTransform =' 
#			print adfGeoTransform[0]
##			print adfGeoTransform[1]
#			print adfGeoTransform[2]
##			print adfGeoTransform[3]
#			print adfGeoTransform[4]
#			print adfGeoTransform[5]

#/* -------------------------------------------------------------------- */
#/*      Report GCPs.                                                    */
#/* -------------------------------------------------------------------- */
	#if bShowGCPs is True and _gdal.GDALGetGCPCount( hDataset ) != None :
		#print 'GCP Projection = ', _gdal.GDALGetGCPProjection(hDataset)
		#for i in range(_gdal.GDALGetGCPCount(hDataset)):
			##const GDAL_GCP      *psGCP;
			#psGCP = _gdal.GDALGetGCPs( hDataset ) + i
		#print 'GCP[',i,']: Id=', psGCP.pszId
		#print 'Info=',psGCP.pszInfo,'(',psGCP.dfGCPPixel,',',psGCP.dfGCPLine,' -> (',psGCP.dfGCPX,',',psGCP.dfGCPY,',', psGCP.dfGCPZ,')'

#/* -------------------------------------------------------------------- */
#/*      Report metadata.                                                */
#/* -------------------------------------------------------------------- */
	papszMetadata = _gdal.GDALGetMetadata( hDataset, 'NULL' )
	if bShowMetadata is True and _gdal.CSLCount(papszMetadata) != None :
		print 'Metadata:'
		for i in range(papszMetadata[i] != None):
			print '  ', papszMetadata[i]
		for iMDD in range(_gdal.CSLCount(papszExtraMDDomains)):
			papszMetadata = _gdal.GDALGetMetadata( hDataset, papszExtraMDDomains[iMDD] )
			if bShowMetadata is True and _gdal.CSLCount(papszMetadata) != None :
				print 'Metadata ', papszExtraMDDomains[iMDD]
				for i in range(papszMetadata[i] != None):
					print '  ', papszMetadata[i]

#/* -------------------------------------------------------------------- */
#/*      Report "IMAGE_STRUCTURE" metadata.                              */
#/* -------------------------------------------------------------------- */
	papszMetadata = _gdal.GDALGetMetadata( hDataset, 'IMAGE_STRUCTURE' )
	if bShowMetadata is True and _gdal.CSLCount(papszMetadata) != None :
		print 'Image Structure Metadata:'
		for i in range(papszMetadata[i] != None):
			print ' ', papszMetadata[i]

#/* -------------------------------------------------------------------- */
#/*      Report subdatasets.                                             */
#/* -------------------------------------------------------------------- */
	papszMetadata = _gdal.GDALGetMetadata( hDataset, 'SUBDATASETS' )
	if _gdal.CSLCount(papszMetadata) != None :
		print 'Subdatasets:'
		for i in range(papszMetadata[i] != None):
			print ' ', papszMetadata[i]

#/* -------------------------------------------------------------------- */
#/*      Report geolocation.                                             */
#/* -------------------------------------------------------------------- */
	papszMetadata = _gdal.GDALGetMetadata( hDataset, 'GEOLOCATION' )
	if _gdal.CSLCount(papszMetadata) != None :
		print 'Geolocation:'
		for i in range(papszMetadata[i] != None):
			print ' ', papszMetadata[i]

#/* -------------------------------------------------------------------- */
#/*      Setup projected to lat/long transform if appropriate.           */
#/* -------------------------------------------------------------------- */
    #if( GDALGetGeoTransform( hDataset, adfGeoTransform ) == CE_None )
        #pszProjection = GDALGetProjectionRef(hDataset);

    #if( pszProjection != NULL && strlen(pszProjection) > 0 )
    #{
        #OGRSpatialReferenceH hProj, hLatLong = NULL;

        #hProj = OSRNewSpatialReference( pszProjection );
        #if( hProj != NULL )
            #hLatLong = OSRCloneGeogCS( hProj );

        #if( hLatLong != NULL )
        #{
            #CPLPushErrorHandler( CPLQuietErrorHandler );
            #hTransform = OCTNewCoordinateTransformation( hProj, hLatLong );
            #CPLPopErrorHandler();
            
            #OSRDestroySpatialReference( hLatLong );
        #}

        #if( hProj != NULL )
            #OSRDestroySpatialReference( hProj );
    #}

#/* -------------------------------------------------------------------- */
#/*      Report corners.                                                 */
#/* -------------------------------------------------------------------- */
    #printf( "Corner Coordinates:\n" );
    #GDALInfoReportCorner( hDataset, hTransform, "Upper Left", 
                          #0.0, 0.0 );
    #GDALInfoReportCorner( hDataset, hTransform, "Lower Left", 
                          #0.0, GDALGetRasterYSize(hDataset));
    #GDALInfoReportCorner( hDataset, hTransform, "Upper Right", 
                          #GDALGetRasterXSize(hDataset), 0.0 );
    #GDALInfoReportCorner( hDataset, hTransform, "Lower Right", 
                          #GDALGetRasterXSize(hDataset), 
                          #GDALGetRasterYSize(hDataset) );
    #GDALInfoReportCorner( hDataset, hTransform, "Center", 
                          #GDALGetRasterXSize(hDataset)/2.0, 
                          #GDALGetRasterYSize(hDataset)/2.0 );

    #if( hTransform != NULL )
    #{
        #OCTDestroyCoordinateTransformation( hTransform );
        #hTransform = NULL;
    #}
    
#/* ==================================================================== */
#/*      Loop over bands.                                                */
#/* ==================================================================== */
    #for( iBand = 0; iBand < GDALGetRasterCount( hDataset ); iBand++ )
    #{
        #double      dfMin, dfMax, adfCMinMax[2], dfNoData;
        #int         bGotMin, bGotMax, bGotNodata, bSuccess;
        #int         nBlockXSize, nBlockYSize, nMaskFlags;
        #double      dfMean, dfStdDev;
        #GDALColorTableH hTable;
        #CPLErr      eErr;

        #hBand = GDALGetRasterBand( hDataset, iBand+1 );

        #if( bSample )
        #{
            #float afSample[10000];
            #int   nCount;

            #nCount = GDALGetRandomRasterSample( hBand, 10000, afSample );
            #printf( "Got %d samples.\n", nCount );
        #}
        
        #GDALGetBlockSize( hBand, &nBlockXSize, &nBlockYSize );
        #printf( "Band %d Block=%dx%d Type=%s, ColorInterp=%s\n", iBand+1,
                #nBlockXSize, nBlockYSize,
                #GDALGetDataTypeName(
                    #GDALGetRasterDataType(hBand)),
                #GDALGetColorInterpretationName(
                    #GDALGetRasterColorInterpretation(hBand)) );

        #if( GDALGetDescription( hBand ) != NULL 
            #&& strlen(GDALGetDescription( hBand )) > 0 )
            #printf( "  Description = %s\n", GDALGetDescription(hBand) );

        #dfMin = GDALGetRasterMinimum( hBand, &bGotMin );
        #dfMax = GDALGetRasterMaximum( hBand, &bGotMax );
        #if( bGotMin || bGotMax || bComputeMinMax )
        #{
            #printf( "  " );
            #if( bGotMin )
                #printf( "Min=%.3f ", dfMin );
            #if( bGotMax )
                #printf( "Max=%.3f ", dfMax );
        
            #if( bComputeMinMax )
            #{
                #GDALComputeRasterMinMax( hBand, False, adfCMinMax );
                #printf( "  Computed Min/Max=%.3f,%.3f", 
                        #adfCMinMax[0], adfCMinMax[1] );
            #}

            #printf( "\n" );
        #}

        #eErr = GDALGetRasterStatistics( hBand, bApproxStats, bStats, 
                                        #&dfMin, &dfMax, &dfMean, &dfStdDev );
        #if( eErr == CE_None )
        #{
            #printf( "  Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f\n",
                    #dfMin, dfMax, dfMean, dfStdDev );
        #}

        #if ( bComputeChecksum)
        #{
            #printf( "  Checksum=%d\n",
                    #GDALChecksumImage(hBand, 0, 0,
                                      #GDALGetRasterXSize(hDataset),
                                      #GDALGetRasterYSize(hDataset)));
        #}

        #dfNoData = GDALGetRasterNoDataValue( hBand, &bGotNodata );
        #if( bGotNodata )
        #{
            #printf( "  NoData Value=%.18g\n", dfNoData );
        #}

        #if( GDALGetOverviewCount(hBand) > 0 )
        #{
            #int         iOverview;

            #printf( "  Overviews: " );
            #for( iOverview = 0; 
                 #iOverview < GDALGetOverviewCount(hBand);
                 #iOverview++ )
            #{
                #GDALRasterBandH hOverview;
                #const char *pszResampling = NULL;

                #if( iOverview != 0 )
                    #printf( ", " );

                #hOverview = GDALGetOverview( hBand, iOverview );
                #printf( "%dx%d", 
                        #GDALGetRasterBandXSize( hOverview ),
                        #GDALGetRasterBandYSize( hOverview ) );

                #pszResampling = 
                    #GDALGetMetadataItem( hOverview, "RESAMPLING", "" );

                #if( pszResampling != NULL 
                    #&& EQUALN(pszResampling,"AVERAGE_BIT2",12) )
                    #printf( "*" );
            #}
            #printf( "\n" );
        #}

        #if( GDALHasArbitraryOverviews( hBand ) )
        #{
            #printf( "  Overviews: arbitrary\n" );
        #}
        
        #nMaskFlags = GDALGetMaskFlags( hBand );
        #if( (nMaskFlags & (GMF_NODATA|GMF_ALL_VALID)) == 0 )
        #{
            #printf( "  Mask Flags: " );
            #if( nMaskFlags & GMF_PER_DATASET )
                #printf( "PER_DATASET " );
            #if( nMaskFlags & GMF_ALPHA )
                #printf( "ALPHA " );
            #if( nMaskFlags & GMF_NODATA )
                #printf( "NODATA " );
            #if( nMaskFlags & GMF_ALL_VALID )
                #printf( "ALL_VALID " );
            #printf( "\n" );
        #}

        #if( strlen(GDALGetRasterUnitType(hBand)) > 0 )
        #{
            #printf( "  Unit Type: %s\n", GDALGetRasterUnitType(hBand) );
        #}

        #if( GDALGetRasterCategoryNames(hBand) != NULL )
        #{
            #char **papszCategories = GDALGetRasterCategoryNames(hBand);
            #int i;

            #printf( "  Categories:\n" );
            #for( i = 0; papszCategories[i] != NULL; i++ )
                #printf( "    %3d: %s\n", i, papszCategories[i] );
        #}

        #if( GDALGetRasterScale( hBand, &bSuccess ) != 1.0 
            #|| GDALGetRasterOffset( hBand, &bSuccess ) != 0.0 )
            #printf( "  Offset: %.15g,   Scale:%.15g\n",
                    #GDALGetRasterOffset( hBand, &bSuccess ),
                    #GDALGetRasterScale( hBand, &bSuccess ) );

        #papszMetadata = GDALGetMetadata( hBand, NULL );
        #if( bShowMetadata && CSLCount(papszMetadata) > 0 )
        #{
            #printf( "  Metadata:\n" );
            #for( i = 0; papszMetadata[i] != NULL; i++ )
            #{
                #printf( "    %s\n", papszMetadata[i] );
            #}
        #}

        #papszMetadata = GDALGetMetadata( hBand, "IMAGE_STRUCTURE" );
        #if( bShowMetadata && CSLCount(papszMetadata) > 0 )
        #{
            #printf( "  Image Structure Metadata:\n" );
            #for( i = 0; papszMetadata[i] != NULL; i++ )
            #{
                #printf( "    %s\n", papszMetadata[i] );
            #}
        #}

        #if( GDALGetRasterColorInterpretation(hBand) == GCI_PaletteIndex 
            #&& (hTable = GDALGetRasterColorTable( hBand )) != NULL )
        #{
            #int                 i;

            #printf( "  Color Table (%s with %d entries)\n", 
                    #GDALGetPaletteInterpretationName(
                        #GDALGetPaletteInterpretation( hTable )), 
                    #GDALGetColorEntryCount( hTable ) );

            #if (bShowColorTable)
            #{
                #for( i = 0; i < GDALGetColorEntryCount( hTable ); i++ )
                #{
                    #GDALColorEntry      sEntry;
    
                    #GDALGetColorEntryAsRGB( hTable, i, &sEntry );
                    #printf( "  %3d: %d,%d,%d,%d\n", 
                            #i, 
                            #sEntry.c1,
                            #sEntry.c2,
                            #sEntry.c3,
                            #sEntry.c4 );
                #}
            #}
        #}

        #if( GDALGetDefaultRAT( hBand ) != NULL )
        #{
            #GDALRasterAttributeTableH hRAT = GDALGetDefaultRAT( hBand );
            
            #GDALRATDumpReadable( hRAT, NULL );
        #}
    #}

    #GDALClose( hDataset );
    
    #CSLDestroy( papszExtraMDDomains );
    #CSLDestroy( argv );
    
    #GDALDumpOpenDatasets( stderr );

    #GDALDestroyDriverManager();

    #CPLDumpSharedList( NULL );
    #CPLCleanupTLS();

    #exit( 0 );
#}

#/************************************************************************/
#/*                        GDALInfoReportCorner()                        */
#/************************************************************************/

#static int 
#GDALInfoReportCorner( GDALDatasetH hDataset, 
                      #OGRCoordinateTransformationH hTransform,
                      #const char * corner_name,
                      #double x, double y )

#{
    #double      dfGeoX, dfGeoY;
    #double      adfGeoTransform[6];
        
    #printf( "%-11s ", corner_name );
    
#/* -------------------------------------------------------------------- */
#/*      Transform the point into georeferenced coordinates.             */
#/* -------------------------------------------------------------------- */
    #if( GDALGetGeoTransform( hDataset, adfGeoTransform ) == CE_None )
    #{
        #dfGeoX = adfGeoTransform[0] + adfGeoTransform[1] * x
            #+ adfGeoTransform[2] * y;
        #dfGeoY = adfGeoTransform[3] + adfGeoTransform[4] * x
            #+ adfGeoTransform[5] * y;
    #}

    #else
    #{
        #printf( "(%7.1f,%7.1f)\n", x, y );
        #return False;
    #}

#/* -------------------------------------------------------------------- */
#/*      Report the georeferenced coordinates.                           */
#/* -------------------------------------------------------------------- */
    #if( ABS(dfGeoX) < 181 && ABS(dfGeoY) < 91 )
    #{
        #printf( "(%12.7f,%12.7f) ", dfGeoX, dfGeoY );

    #}
    #else
    #{
        #printf( "(%12.3f,%12.3f) ", dfGeoX, dfGeoY );
    #}

#/* -------------------------------------------------------------------- */
#/*      Transform to latlong and report.                                */
#/* -------------------------------------------------------------------- */
    #if( hTransform != NULL 
        #&& OCTTransform(hTransform,1,&dfGeoX,&dfGeoY,NULL) )
    #{
        
        #printf( "(%s,", GDALDecToDMS( dfGeoX, "Long", 2 ) );
        #printf( "%s)", GDALDecToDMS( dfGeoY, "Lat", 2 ) );
    #}

    #printf( "\n" );

    #return True;
#} 

#include <stdio.h>
#include <stdlib.h>
#include "mfhdf.h"

# define NUM_X	100
# define NUM_Y	3000
# define num_Z	20

int main(int argc, char *argv[]){
	char	filename[100], sds_name[100];
	int32	file_ID, sds_ID, index0[3], index1[3];
	int	which_sds=0, i,j,k;
	float32	data[NUM_X][NUM_Y][NUM_Z];

	/*Number of scans = num_x*/
	int num_x;
	/*Number of scans = num_y?*/
	int num_y;
	/*Number of scans = num_z?*/
	int num_z;
	

	index0[0] = 0;
	index0[1] = 0;
	index0[2] = 0;
	index1[0] = 0;
	index1[1] = 0;
	index1[2] = 0;

	if(argc != 3){
		printf( "\n usage: read_sds <filename> <sds_name>\n\n" );
		exit(1);
	} else {
		strcpy( filename, argv[1] );
		strcpy( sds_name, argv[2] );
	}
	/*
	* Read Data
	*/

// 	if( Hishdf(filename) != TRUE ){
// 		printf( "error: file is not HDF... \n %s \n", filename);
// 		exit(1);
// 	}
	
	file_ID 	= SDstart( filename, DFACC_READ );
	which_sds	= SDnametoindex( file_ID, sds_name );

	if (which_sds == FAIL ){
		printf( "error: sds_name '%s' does not exist...\n", filename );
		exit(1);
	}

	sds_ID	= SDselect( file_ID, which_sds );
	SDreaddata( sds_ID, index0, NULL, index1, (VOIDP)data );
	SDendaccess( sds_ID );
	SDend( file_ID );
	printf("index0 = %f %f %f\n", index0[0], index0[1], index0[2]);
	printf("index1 = %f %f %f\n", index1[0], index1[1], index1[2]);
	/*
	* print out data
	*/

	for( i=0 ; i<num_x ; i++ ){
		for( j=0 ; j<num_y ; j++ ){
			for( k=0 ; k<num_z ; k++ ){
				printf( "  %s(%d,%d,%d) = %15f \n", sds_name, i,j,k, data[i][j][k] );
			}
		}
	}

	exit(0);
}

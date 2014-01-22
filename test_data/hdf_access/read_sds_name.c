#include <stdio.h>
#include <stdlib.h>
#include "mfhdf.h"

# define MAX_NUM_SDS	300
# define MAX_NUM_DIM	5

int main(int argc, char *argv[]){
	char	filename[100], sds_name[100][MAX_NUM_SDS];
	int32	file_ID, sds_ID, num_sds, num_file_attribute;
	int	which_sds=0, i;

	char	name[100], type_name[100];
	int32	num_dim, dim_size[MAX_NUM_DIM];
	int32	data_type, num_sds_attribute;

	strcpy( filename, "2B31.070101.52026.6.HDF");

	/*
	* Read Data
	*/

	file_ID 	= SDstart( filename, DFACC_READ );
	sds_ID		= SDfileinfo( file_ID, &num_sds, &num_file_attribute );

	printf( "\n there are %d SDSs in the file.\n", num_sds );

	for( which_sds=0 ; which_sds<num_sds ; which_sds++ ){
		sds_ID	= SDselect( file_ID, which_sds );
		SDgetinfo( sds_ID, name, &num_dim, dim_size, &data_type, &num_sds_attribute );
		SDendaccess( sds_ID );
	
		switch (data_type){
			case 5: strcpy( type_name, "float32" ); break;
			case 20: strcpy( type_name, "int8" ); break;
			case 22: strcpy( type_name, "int16" ); break;
			case 24: strcpy( type_name, "int32" ); break;
			default: strcpy( type_name, "other" ); break;
		}
		
		strcpy( sds_name[which_sds], name );
		printf( "%3d %10s %20s(", which_sds, type_name, sds_name[which_sds] );
		for(i=0;i<num_dim;i++){
			printf("%5d, ", dim_size[i]);
		}
		printf( ")\n" );
	}
	SDend( file_ID );
	exit(0);
}

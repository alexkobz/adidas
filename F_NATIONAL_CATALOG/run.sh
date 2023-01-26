#!/bin/bash
#
##	\author		kobzaale
##	\descr      Integration with National Catalog
##	\jira		https://tools.adidas-group.com/jira/browse/CB-7531
##	\jira		https://tools.adidas-group.com/jira/browse/CB-7631

BASEFOLDERCSV=~/etl_data/national_catalog/
apikey=''
offset=0

python_run $work_dir/00.api_national_catalog.py $BASEFOLDERCSV $apikey $offset
exa_run $work_dir/01.INSERT_STG_NATIONAL_CATALOG.sql -- "$etl_server" "$etl_user" "$etl_password"
exa_run $work_dir/02.MERGE_LU_TABLES.sql
exa_run $work_dir/03.MERGE_F_NATIONAL_CATALOG.sql
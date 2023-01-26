#!/bin/bash
#
##  \author		kobzaale
##	\descr		Integration with Russian Post
##	\jira		https://tools.adidas-group.com/jira/browse/CB-7493
#

BASEFOLDER=~/etl_data/ecom_russian_post/
login=''
password=''

exa_run $work_dir/01.EXPORT_SHIPMENT_NO.sql -- "$etl_server" "$etl_user" "$etl_password"
python_run $work_dir/russian_post.py $BASEFOLDER $login $password
exa_run $work_dir/02.LOAD_HST_ECOM_RUSSIAN_POST.sql -- "$etl_server" "$etl_user" "$etl_password"
exa_run $work_dir/03.MERGE_F_ECOM_COURIER.sql
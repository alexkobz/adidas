#!/bin/bash
#
##	\author		kobzaale
##	\descr		eCom Gross Demand forecast, hourly, SARIMAX

exa_run $work_dir/01.ECOM_SALE_OUTLIERS.sql

if [ "$current_inst" == "prod" ]
then
    dsn=""
    schema=""
    user=""
    password=""
else
    dsn=""
    schema=""
    user=""
    password=""
fi

for ecom_shop in 1 2
do
    python_run $work_dir/02.ECOM_HOURLY_GROSS_DEMAND_FORECAST.py $dsn $schema $user $password $ecom_shop
done

exa_run $work_dir/03.MERGE_F_ECOM_FORECAST.sql
exa_run $work_dir/04.INSERT_TMP_ECOM_FORECAST.sql

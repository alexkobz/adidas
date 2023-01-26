#!/bin/bash
#
##  \author		kobzaale
##	\descr		Report Bizagi SLA
##	\jira		https://jira.tools.3stripes.net/browse/CB-7550
#

exa_run $work_dir/01.IMPORT_STG_BIZAGI_CASE.sql
exa_run $work_dir/02.MERGE_BIZAGI_CASE.sql

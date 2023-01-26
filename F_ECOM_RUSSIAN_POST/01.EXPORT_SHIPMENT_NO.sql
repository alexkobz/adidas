EXPORT (
    SELECT *
    FROM (
        IMPORT INTO (
            DELIVERY_NOTE_NO     VARCHAR(35) UTF8,
            TRACKER_NO         VARCHAR(50) UTF8
        )
        FROM JDBC
        AT CIS_WMS_RU
        STATEMENT '
            select
                rl.[Order No_] as DELIVERY_NOTE_NO,
                rl.[Tracker No_] as TRACKER_NO
            from [NAVCIS_RU_ANALYSIS].dbo.[adidas WH 2006$Courier Request Line] rl
            inner join [NAVCIS_RU_ANALYSIS].dbo.[adidas WH 2006$Courier Request Header] rh on rl.[Document No_] = rh.[No_]
            where rh.[Courier Code] = ''###''
        '
    )
    WHERE TRACKER_NO IS NOT NULL
)
INTO CSV
AT '&1'
USER '&2'
IDENTIFIED BY '&3'
FILE '~/etl_data/ecom_russian_post/shipment_in.csv'
REPLACE
COLUMN SEPARATOR = ';'
COLUMN DELIMITER = ''
WITH COLUMN NAMES
;

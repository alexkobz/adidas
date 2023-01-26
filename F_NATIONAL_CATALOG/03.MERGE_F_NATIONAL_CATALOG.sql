MERGE INTO F_NATIONAL_CATALOG DST
USING (
    SELECT
        LE.EAN_ID,
        STG.GOOD_NAME,
        LT.TNVED_ID,
        STG.GOOD_STATUS,
        LC.DATE_ID
    FROM STG_NATIONAL_CATALOG STG
    JOIN LU_EAN LE ON STG.GTIN = LE.EAN_NO
    JOIN LU_TNVED LT ON STG.TNVED = LT.TNVED_NO
    JOIN LU_CALENDAR LC ON STG.UPDATED_DATE = LC.DATE_ID
) SRC ON
    DST.EAN_ID = SRC.EAN_ID
WHEN MATCHED THEN UPDATE SET
	DST.GOOD_NAME = SRC.GOOD_NAME,
	DST.TNVED_ID = SRC.TNVED_ID,
	DST.GOOD_STATUS = SRC.GOOD_STATUS,
	DST.DATE_ID = SRC.DATE_ID
WHEN NOT MATCHED THEN INSERT (
    EAN_ID,
    GOOD_NAME,
    TNVED_ID,
    GOOD_STATUS,
    DATE_ID
)
VALUES (
    SRC.EAN_ID,
    SRC.GOOD_NAME,
    SRC.TNVED_ID,
    SRC.GOOD_STATUS,
    SRC.DATE_ID
)
;

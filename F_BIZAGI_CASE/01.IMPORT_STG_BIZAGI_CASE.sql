TRUNCATE TABLE STG_LU_BIZAGI_CASE
;

IMPORT INTO STG_LU_BIZAGI_CASE (
	BIZAGI_CASE_NO,
    BIZAGI_CASE_INITIATOR_ID,
	BIZAGI_CASE_INITIATOR_LOGIN,
	BIZAGI_CASE_INITIATOR_NAME,
	BIZAGI_CASE_CREATION_DATE,
	BIZAGI_DEPARTMENT_NAME_INT,
	BIZAGI_PURCHASE_TYPE_NAME_INT,
	BIZAGI_PURCHASE_FORMAT_NAME_INT,
	BIZAGI_IO,
	PNL_COST_CENTER_CODE,
	BIZAGI_PLANNED_DELIVERY_DATETIME,
	BIZAGI_AMOUNT_WOVAT,
	CURRENCY_CODE,
	BIZAGI_AMOUNT_INIT_LCY,
	BIZAGI_AMOUNT_TEND_LCY,
	BIZAGI_VENDOR_CUSTOM,
	BIZAGI_VENDOR_NAME_LOCAL,
	BIZAGI_APPROVED_VENDOR_CUSTOM,
	BIZAGI_VENDOR1_NAME_LOCAL,
	BIZAGI_CONTRACT_TYPE_NAME_INT,
	BIZAGI_COMPANY_INVITED,
	BIZAGI_RECEIVED_OFFER,
	BIZAGI_FIRST_OFFER_AMOUNT_VAT,
	BIZAGI_AVERAGE_AMOUNT_VAT,
	BIZAGI_TAX_REFERENCE_NO,
	BIZAGI_CASE_DESCRIPTION,
	BIZAGI_END_CONTRACT_DATETIME
)
FROM JDBC AT CIS_BIZAGI
STATEMENT '
	SELECT
		[CaseNumber],
        [IDEmployee],
        [InitiatorUserName],
		[CaseInitiator],
        [CreationDate],
		[Department],
		[PurchaseType],
        [PurchaseFormat],
		[IO],
		[CostCenter],
		[DeliveryDate],
		[AmountRub],
		[Currency],
		[AmountInit],
		[AmountTender],
		[Vendor Custom text],
		[VendorName],
		[ApprovedVendortxt],
		[Vendor1Name],
		[ContractType],
		[CompaniesInvited],
		[ReceivedOffers],
		[FirstOfferAmountwoVAT],
		[AverageAmountwoVAT],
		[TaxReferenceNumber],
		[Description],
		[EndContractDate]
	FROM [CIS_WFAdidas].[dbo].[vContractsApprovalCaseDetails]
	WHERE [CaseNumber] IS NOT NULL
	;
'
;

TRUNCATE TABLE STG_F_BIZAGI_CASE_PURCHASE_CONTRACT
;

IMPORT INTO STG_F_BIZAGI_CASE_PURCHASE_CONTRACT (
	BIZAGI_APPROVEMENT_ID,
    BIZAGI_CASE_NO,
    BIZAGI_CASE_DATE,
    BIZAGI_EMPLOYEE_NAME,
    BIZAGI_EMPLOYEE_LOGIN,
    BIZAGI_EMPLOYEE_ID,
    BIZAGI_COUNTRY_NAME_INT,
    BIZAGI_TASK_NAME,
    BIZAGI_RESOLUTION,
    BIZAGI_OBSERVATION,
    BIZAGI_PROCESS,
    BIZAGI_PURCHASE_CONTRACT
)
FROM JDBC AT CIS_BIZAGI
STATEMENT'
	SELECT
       [idApprovementHistory],
       [CaseNumber],
       [OnDate],
       [Performer],
       [Login],
       [IDEmployee],
       [Country],
       [TaskName],
       [Resolution],
       [Observation],
       [ProcessName],
       [PurchaseContract]
    FROM [CIS_WFAdidas].[dbo].[vApprovalHistoryPurchase]
	;
'
;

TRUNCATE TABLE STG_F_BIZAGI_CASE
;

IMPORT INTO STG_F_BIZAGI_CASE (
	BIZAGI_CASE_NO,
	BIZAGI_TASK_STATUS_NAME_INT,
	BIZAGI_TASK_STATUS_NO,
	EMPLOYEE_NAME_INT,
	EMPLOYEE_LOGIN,
	BIZAGI_DEPARTMENT_NAME_INT,
	BIZAGI_WI_ENTRY_DATETIME,
	BIZAGI_CASE_DURATION,
	BIZAGI_WI_SOLUTION_DATETIME,
	BIZAGI_WI_ESTIMATED_SOLUTION_DATETIME,
	BIZAGI_SLA_MINUTES,
	BIZAGI_STATE_NAME_INT
)
FROM JDBC AT CIS_BIZAGI
STATEMENT
'
	SELECT
		radNumber,
		tskDisplayName,
		idTask,
		fullName,
		userName,
		[Approver Department],
		wiEntryDate,
		Duration,
		wiSolutionDate,
		wiEstimatedSolutionDate,
		SLA,
		State
	FROM vContractsApprovalReportSLA
	where [wiSolutionDate] is not null
	;
'
;

truncate table TMP_BIZAGI_CLOSED_CASE;

IMPORT INTO TMP_BIZAGI_CLOSED_CASE (
   BIZAGI_CASE_NO
)
FROM JDBC AT CIS_BIZAGI
STATEMENT '
   SELECT distinct
      [idCase]
   FROM [CIS_WFAdidas].[dbo].[vBI_СlosedCases]
   WHERE [idCase] IS NOT NULL
   ;
'
;

weekly = 'KRAFT_STORE_SKU_PROJ_AGG_(WEEKS)'
monthly = 'KRAFT_STORE_SKU_PROJ_AGG_(GREGMONTH)(P)'

weeks = """
SELECT
AggValue as SKU,
STARTDATE,
CovDur,
CAST((CsInventory*NET_WEIGHT) as decimal(14,0)) as ProjOH,
CAST((CsDemand*NET_WEIGHT)as decimal(14,0)) as TotDmd,
CAST((CsDepDmd*NET_WEIGHT)as decimal(14,0)) as DepDmd,
CAST((Production*NET_WEIGHT)as decimal(14,0)) as TotSupply
FROM (
SELECT
        AggValue,
        STARTDATE,
        CAST(SUM(ProjOH)as decimal(14,0)) as CsInventory,
        CAST(SUM(covdur/(1440)) as decimal(14,2)) as CovDur,
        CAST(SUM(totdmd) as decimal(14,0)) as CsDemand,
        CAST(SUM(depdmd) as decimal(14,0)) as CsDepDmd,
        CAST(SUM((PlanOrders + FirmPlanOrder + SchedRcpts)) as decimal(14,0))  AS PRODUCTION,
        CAST(SUM(IMPORT_ITEM.NET_WT_CSE_QTY) as DECIMAL(14,1)) as NET_WEIGHT
FROM aggskuprojstatic
INNER JOIN
    IMPORT_ITEM
ON
    IMPORT_ITEM.KGF_STD_ITEM_CDE=AggValue
  WHERE optionset='{}'
  AND UDC_BUSN_SEGM_DESC in ('SNACKS', 'Foodservice')
  GROUP BY AggValue, startdate
)
ORDER BY AggValue, STARTDATE
""".format(weekly)



################################################################################


months = """
SELECT
AggValue as SKU,
STARTDATE,
CovDur,
CAST((CsInventory*NET_WEIGHT) as decimal(14,0)) as ProjOH,
CAST((CsDemand*NET_WEIGHT)as decimal(14,0)) as TotDmd,
CAST((CsDepDmd*NET_WEIGHT)as decimal(14,0)) as DepDmd,
CAST((Production*NET_WEIGHT)as decimal(14,0)) as TotSupply
FROM (
SELECT
        AggValue,
        STARTDATE,
        CAST(SUM(ProjOH)as decimal(14,0)) as CsInventory,
        CAST(SUM(covdur/(1440)) as decimal(14,2)) as CovDur,
        CAST(SUM(totdmd) as decimal(14,0)) as CsDemand,
        CAST(SUM(depdmd) as decimal(14,0)) as CsDepDmd,
        CAST(SUM((PlanOrders + FirmPlanOrder + SchedRcpts)) as decimal(14,0))  AS PRODUCTION,
        CAST(SUM(IMPORT_ITEM.NET_WT_CSE_QTY) as DECIMAL(14,1)) as NET_WEIGHT
FROM aggskuprojstatic
INNER JOIN
    IMPORT_ITEM
ON
    IMPORT_ITEM.KGF_STD_ITEM_CDE=AggValue
  WHERE optionset='{}'
  AND UDC_BUSN_SEGM_DESC in ('SNACKS', 'Foodservice')
  GROUP BY AggValue, startdate
)
ORDER BY AggValue, STARTDATE
""".format(monthly)

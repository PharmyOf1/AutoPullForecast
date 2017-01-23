import pyodbc, openpyxl
import pandas as pd
import numpy as np
import datetime
import acct_months_hash as q
from queries import weeks, months
from creds import conn

cursor = conn.cursor()

def data(sql,conn, measure=""):
    df = pd.read_sql(sql, conn)
    if measure  == "ACCT":
        df = adjust_to_acct(df)
    else:
        df['date'] = pd.to_datetime(df.STARTDATE)
    return df

def adjust_to_acct(df):
    df['STARTDATE'] = pd.to_datetime(df.STARTDATE)
    df['date'] = (df['STARTDATE'].map(q.get_month))
    df['date'] = pd.to_datetime(df.date)
    return df

def transform_data(df):
    df = df.groupby([df.SKU,df.date]).agg({'COVDUR':['first'], 'PROJOH':['first'],'TOTDMD':['sum'],'DEPDMD':['sum'],'TOTSUPPLY':['sum']})
    df.columns = df.columns.get_level_values(0)
    df = df.stack().reset_index()
    df.columns = ['SKU', 'MONTH', 'MEASURE','VALUE']
    df = df.pivot_table(index=['SKU','MEASURE'], columns=['MONTH'], aggfunc=sum)
    df.columns = df.columns.get_level_values(1)
    return df

def save_to_file(list_dfs):
    day, month, year  = datetime.datetime.now().day,datetime.datetime.now().month,datetime.datetime.now().year
    xls_path = 'C:\\Users\\UNA0464\\Desktop\\MDLZ Roles\\Capacity Planning\\Ad Hoc\\AutoPullForecast\\PSIs\\FULL PSI {}-{}-{}.xlsx'.format(month,day,year)
    writer = pd.ExcelWriter(xls_path)
    list_dfs[0].to_excel(writer,'WEEKS')
    list_dfs[1].to_excel(writer,'GREGORIAN')
    list_dfs[2].to_excel(writer,'ACCT')
    writer.save()

    format_xl(xls_path)

def format_xl(xl):
    wb = openpyxl.load_workbook(xl)
    sheets = [wb[s] for s in wb.get_sheet_names()]
    for sheet in sheets:
        r, c = sheet.max_row, sheet.max_column
        sheet.freeze_panes = 'A2'
        for i in range(1,c+1):
            sheet.cell(row=1,column=i).number_format = "M/DD/YY"

        #Unmerge
        m = sheet._merged_cells.copy()
        for merged_row in m:
            sheet.unmerge_cells(merged_row)

        #Add formula to previous cell
        for i in range(r,0,-1):
            if not sheet.cell(row=i,column=1).value:
                sheet.cell(row=i,column=1).value = "=A{}".format(i-1)

        sheet.column_dimensions["A"].width = 15

    wb.save(xl)


if __name__ == '__main__':
    weeks_data = data(weeks,conn)
    greg_data = data(months,conn)

    df_weeks = transform_data(weeks_data)
    df_greg = transform_data(greg_data)
    df_acct = transform_data(data(weeks,conn,"ACCT"))

    save_to_file([df_weeks,df_greg,df_acct])
    print ("Data Transfer: Success")

from datetime import date, datetime
from copy import deepcopy
import math
import numpy as np
import pandas as pd
import sqlite3
from bokeh.models import ColumnDataSource
from bokeh.models.annotations import Title
from plots import divs_key_numbers

def calc_key_numbers(cdsQC):
    
    if len(cdsQC.data['raw_file']) > 0:
        latestDate = max(cdsQC.data['dt_form'])
        latestIDX = [i for i, j in enumerate(cdsQC.data['dt_form']) if j == latestDate][0]
        latestFile = cdsQC.data['raw_file'][latestIDX][:-4]
        latestPSMs = cdsQC.data['psm_number'][latestIDX]
    
        maxPSMs = max(cdsQC.data['psm_number'])
        nEntries = len(cdsQC.data['raw_file'])
        outlist = [latestFile, latestPSMs, maxPSMs, nEntries]
    else:
        outlist = ['None', 0, 0, 0]
    
    return outlist

def read_qc_table(dbPath, tableName):
    conn = sqlite3.connect(dbPath)
    conn.execute("PRAGMA foreign_keys = ON")
    sqlQ = f'SELECT * FROM {tableName}'
    df = pd.read_sql_query(sqlQ, conn)
    df['dt_form'] = pd.to_datetime(df['file_date'], format='%m/%d/%Y %I:%M:%S %p')
    df['msms/1000'] = df['msms_number']/1000
    df['id_rate_perc'] = df['id_rate']*100
    df.sort_values(by='dt_form', inplace=True)
    print(f'Fetched QC data frame for {tableName} of size', df.shape)
    cdsQC = ColumnDataSource(df)
    
    try:
        sqlQ = f'SELECT * FROM service'
        dfS = pd.read_sql_query(sqlQ, conn)
        dfS['dt_form'] = pd.to_datetime(dfS['date'], format='%d/%m/%Y')
        dfS = dfS[ ( dfS['dt_form'] >= min(df['dt_form']) ) &
                  ( dfS['dt_form'] <= max(df['dt_form']) ) ]
        print('Fetched servicing data frame of size', dfS.shape)
        cdsService = ColumnDataSource(dfS)
    except:
        print('Could not fetch information about service')
        cdsService = ColumnDataSource( { 'procedure_id':[],'date':[],
                                       'type':[],'is_pm':[],'comment':[],
                                       'dt_form':[] } )
        
    conn.close()
    
    return cdsQC, cdsService

def update_qc_table(cdsQC, cdsService, instrDBDict, newInstr, keyNumDivs):
    dbPath, tableName = instrDBDict[newInstr]
    newQC, newServ = read_qc_table(dbPath, tableName)
    cdsQC.data = dict(newQC.data)
    cdsService.data = dict(newServ.data)
    
    newKeyNumbers = calc_key_numbers(cdsQC)
    newBoxes = divs_key_numbers(cdsQC, *newKeyNumbers)
    for i, div in enumerate(keyNumDivs):
        div.text = newBoxes[i].text


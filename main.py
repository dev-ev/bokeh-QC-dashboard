from funcs import calc_key_numbers, read_qc_table, update_qc_table
from plots import divs_key_numbers, instr_selector
from plots import qc_text, qcplots_global, qcplots_timed
from bokeh.io import output_file, show
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Legend, Select
from bokeh.models.widgets import Div
from bokeh.plotting import figure, curdoc

dbPath = "/home/trainee/Documents/SQL_Project_DB/FilesDB_Simulated_200725.db"

qcDbPaths = {'Lumos': '/mnt/protoeomics/Lumos/QC/QC_Reports/QC_DB/qc_lumos_st191029.db',
             'Fusion': '/mnt/protoeomics/Fusion/QC/QC_Reports/QC_DB/qc_fusion_st191029.db',
             'QEHF': '/mnt/protoeomics/QExactive HF/QC/QC_Reports/QC_DB/qc_qehf_st191107.db'}
qcInstrDBs = {'Lumos': (qcDbPaths['Lumos'],'lumos'),
              'Lumos_FAIMS': (qcDbPaths['Lumos'],'lumos_faims'),
              'Fusion': (qcDbPaths['Fusion'],'fusion'),
              'QEHF': (qcDbPaths['QEHF'],'qehf')}

#Sidebar width
SIDEWIDTH = 200
#Width of the main page with plots
MAIN_WIDTH = 1000
#Search engine to be entered manually at this point.
SENGINE = 'Mascot'

qcTabTxt = qc_text(width=SIDEWIDTH)
allInstrs = list(qcInstrDBs.keys())
cdsQC, cdsServ = read_qc_table(qcInstrDBs[allInstrs[0]][0], qcInstrDBs[allInstrs[0]][1])
keyNums = calc_key_numbers(cdsQC)
txtBoxes = divs_key_numbers(cdsQC, *keyNums)
selectInstr = instr_selector(allInstrs, allInstrs[0], width=SIDEWIDTH)
selectInstr.on_change( 'value', lambda _,__,newInstr: update_qc_table(cdsQC, cdsServ,
                                                                      qcInstrDBs, newInstr, txtBoxes) )
servD, pQCPSM, pIdMsms, pIT, pMzErr, pErrStd, pPW, pAbund, pSES, pRTs = qcplots_timed(cdsQC, cdsServ,
                                                                               full_width=MAIN_WIDTH, seng=SENGINE)
txtPSc, pSc1, pSc2 = qcplots_global(cdsQC, full_width=MAIN_WIDTH, seng=SENGINE)

curdoc().title = 'QC Dashboard'
sm = 'stretch_width'
curdoc().add_root(row( column(qcTabTxt, selectInstr),
                       column(row(*txtBoxes),
                              servD,
                              row(pQCPSM, pIdMsms, sizing_mode=sm),
                              row(pMzErr, pErrStd, sizing_mode=sm),
                              row(pPW, pIT, sizing_mode=sm),
                              row(pAbund, pSES, sizing_mode=sm),
                              pRTs,
                              txtPSc,
                              row(pSc1, pSc2, sizing_mode=sm),
                              sizing_mode=sm) ) )

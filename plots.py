import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool, Legend, Range1d, Select
from bokeh.models.widgets import Div
from bokeh.plotting import figure

def divs_key_numbers(cdsQC, latestFile, latestPSMs, maxPSMs, nEntries):
    width1 = 250
    width2 = 150
    HEIGHT = 60
    
    txtBox1 = Div(text=('<span style="color:#ff9100;font-size:12px">LATEST FILE</span><br>' +
                        f'<span style="color:#ff9100;font-size:20px;font-weight:bold">{latestFile}</span>'),
                margin=(20,10,20,10),
                width=width1, height=HEIGHT)
    txtBox2 = Div(text=('<span style="color:#ff9100;font-size:12px">LATEST PSMs</span><br>' +
                        f'<span style="color:#ff9100;font-size:20px;font-weight:bold">{latestPSMs}</span>'),
                margin=(20,10,20,10),
                width=width2, height=HEIGHT)

    txtBox3 = Div(text=('<span style="font-size:12px">ALL-TIME MAX PSMs</span><br>' +
                        f'<span style="font-size:20px;font-weight:bold">{maxPSMs}</span>'),
                margin=(20,10,20,10),
                width=width2, height=HEIGHT)
    txtBox4 = Div(text=('<span style="font-size:12px">ENTRIES IN DB</span><br>' +
                        f'<span style="font-size:20px;font-weight:bold">{nEntries}</span>'),
                margin=(20,10,20,10),
                width=width2, height=HEIGHT)

    return [txtBox1, txtBox2, txtBox3, txtBox4]

def instr_selector(allInstrs, defaultInstr, width=200):
    selectInstr = Select(title='Select instrument:',
                        value=defaultInstr, options=allInstrs,
                        sizing_mode='fixed', height=50, width=width,
                        margin=(20,20,20,20))    
    return selectInstr

def qc_text(width=200):
    qcPlotText = Div(text='<b>QC Dashboard</b>', margin=(20,20,10,20),
                     width=width)
    qcPlotText.style = {'width': f'{width}px',
                        #'font-style': 'bold',
                        'font-size': '24px', 
                        #'color': 'white',
                        #'background-color': '#8f72c2',
                        #'padding-top': '20px',
                        #'padding-bottom': '20px',
                        #'padding-left': '2px',
                        'box-sizing': 'border-box'
                        }
    return qcPlotText

def qcplots_timed(cdsQC, cdsServ, full_width=1000, seng='Mascot'):
    eachWidth = int(full_width / 2)
    EACH_HEIGHT = 350
    SERVD_HEIGHT = 120
    LINE_W = 3
    #Take the background color from the index.html to match the background of the page
    PLOT_BGR_COL = '#151b5c'
    commonToolstring = 'box_zoom,xwheel_zoom,xpan,reset,save'
    
    tooltips = [('File', '@raw_file'), ('PSMs', '@psm_number'), ('Peptides', '@peptide_number')]
    pQCPSM = figure(plot_width=eachWidth, plot_height=EACH_HEIGHT, x_axis_type='datetime',
                    tools=commonToolstring, active_drag='box_zoom', toolbar_location='right',
                    tooltips=tooltips)
    pQCPSM.add_layout(Legend(), 'above')
    pQCPSM.line(x='dt_form', y='psm_number', color='navy', alpha=0.5,
                line_width = LINE_W, legend_label='PSMs', source=cdsQC)
    pQCPSM.circle(x='dt_form', y='psm_number', color='navy', alpha=0.5, size = 8, source=cdsQC)
    pQCPSM.yaxis.axis_label = 'PSMs'
    #Set the repeated style elements to each QC plot
    def add_repeated_elements(plotObj):
        #plotObj.border_fill_color = "whitesmoke"
        plotObj.border_fill_color = '#e8e8ed'
        plotObj.min_border_left = 80
        plotObj.min_border_right = 50
        plotObj.background_fill_color = '#e8e8ed'
        plotObj.legend.location = 'bottom_left'
        plotObj.legend.background_fill_alpha = 0
        plotObj.xaxis.axis_label = 'Date'
        plotObj.xaxis.axis_label_text_font_size = '16px'
        plotObj.yaxis.axis_label_text_font_size = '16px'
        plotObj.xaxis.major_label_text_font_size = '12px'
        plotObj.yaxis.major_label_text_font_size = '12px'
        
    add_repeated_elements(pQCPSM)
    
    tooltips = [('File', '@raw_file'), ('ID rate %', '@id_rate_perc'),
                ('MSMS spectra', '@msms_number'), ('PSMs', '@psm_number')]
    pIdMsms = figure(plot_width=eachWidth, plot_height=EACH_HEIGHT, x_axis_type='datetime',
                    x_range=pQCPSM.x_range, tools=commonToolstring,
                    active_drag='box_zoom', toolbar_location='right', tooltips=tooltips)
    pIdMsms.add_layout(Legend(), 'above')
    pIdMsms.line(x='dt_form', y='msms/1000', color='#96730f', alpha=0.5,
                line_width = LINE_W, legend_label='MSMS/1000', source=cdsQC)
    pIdMsms.line(x='dt_form', y='id_rate_perc', color='#1f0f96', alpha=0.5,
                line_width = LINE_W, legend_label='ID rate %', source=cdsQC)
    add_repeated_elements(pIdMsms)

    tooltips = [('File', '@raw_file'), ('Mean IT, ms', '@mean_psm_it_ms'),
                ('PSMs', '@psm_number')]
    pInjTimes = figure(plot_width=eachWidth, plot_height=EACH_HEIGHT, x_axis_type='datetime',
                    x_range=pQCPSM.x_range, tools=commonToolstring,
                    active_drag='box_zoom', toolbar_location='right', tooltips=tooltips)
    pInjTimes.add_layout(Legend(), 'above')
    pInjTimes.line(x='dt_form', y='mean_psm_it_ms', color='#9600b0', alpha=0.5,
                line_width = LINE_W, legend_label='Mean PSM IT', source=cdsQC)
    pInjTimes.yaxis.axis_label = 'PSM Inj. Times, ms'
    add_repeated_elements(pInjTimes)
    pInjTimes.legend.location = 'top_left'
    
    tooltips = [('File', '@raw_file'), ('Mean m/z error, ppm', '@mean_mz_err_ppm'),
                ('M/Z error st. dev', '@mz_err_ppm_stdev'), ('PSMs', '@psm_number')]
    pMzErr = figure(plot_width=eachWidth, plot_height=EACH_HEIGHT, x_axis_type='datetime',
                    x_range=pQCPSM.x_range, tools=commonToolstring,
                    active_drag='box_zoom', toolbar_location='right', tooltips=tooltips)
    pMzErr.add_layout(Legend(), 'above')
    pMzErr.line(x='dt_form', y='mean_mz_err_ppm', color='#b00000', alpha=0.5,
                line_width = LINE_W, legend_label='Mean m/z error', source=cdsQC)
    pMzErr.yaxis.axis_label = 'M/Z error, ppm'
    add_repeated_elements(pMzErr)
    
    tooltips = [('File', '@raw_file'), ('Mean m/z error, ppm', '@mean_mz_err_ppm'),
                ('M/Z error st. dev', '@mz_err_ppm_stdev'), ('PSMs', '@psm_number')]
    pMzErrStd = figure(plot_width=eachWidth, plot_height=EACH_HEIGHT, x_axis_type='datetime',
                    x_range=pQCPSM.x_range, tools=commonToolstring,
                    active_drag='box_zoom', toolbar_location='right', tooltips=tooltips)
    pMzErrStd.add_layout(Legend(), 'above')
    pMzErrStd.line(x='dt_form', y='mz_err_ppm_stdev', color='#96730f', alpha=0.5,
                line_width = LINE_W, legend_label='M/Z error standard deviation', source=cdsQC)
    pMzErrStd.yaxis.axis_label = 'M/Z error std. dev, ppm'
    add_repeated_elements(pMzErrStd)

    tooltips = [('File', '@raw_file'), ('Mean peak width, s', '@mean_peak_width'),
                ('PSMs', '@psm_number')]
    pPWidth = figure(plot_width=eachWidth, plot_height=EACH_HEIGHT, x_axis_type='datetime',
                    x_range=pQCPSM.x_range, tools=commonToolstring,
                    active_drag='box_zoom', toolbar_location='right', tooltips=tooltips)
    pPWidth.add_layout(Legend(), 'above')
    pPWidth.line(x='dt_form', y='mean_peak_width', color='#0008eb', alpha=0.5,
                line_width = LINE_W, legend_label='Mean peak width', source=cdsQC)
    pPWidth.yaxis.axis_label = 'Peak width, s'
    add_repeated_elements(pPWidth)
    
    tooltips = [('File', '@raw_file'), ('Mean precursor int', '@mean_prec_intensity'),
                ('PSMs', '@psm_number')]
    pAbund = figure(plot_width=eachWidth, plot_height=EACH_HEIGHT, x_axis_type='datetime',
                    x_range=pQCPSM.x_range, tools=commonToolstring,
                    active_drag='box_zoom', toolbar_location='right', tooltips=tooltips)
    pAbund.add_layout(Legend(), 'above')
    pAbund.line(x='dt_form', y='mean_prec_intensity', color='#0008eb', alpha=0.5,
                line_width = LINE_W, legend_label='Mean precursor intensity', source=cdsQC)
    pAbund.yaxis.axis_label = 'Precursor intensity'
    add_repeated_elements(pAbund)
    
    tooltips = [('File', '@raw_file'), (f'Score {seng}', '@mean_sengine_score'),
                ('PSMs', '@psm_number')]
    pSES = figure(plot_width=eachWidth, plot_height=EACH_HEIGHT, x_axis_type='datetime',
                    x_range=pQCPSM.x_range, tools=commonToolstring,
                    active_drag='box_zoom', toolbar_location='right', tooltips=tooltips)
    pSES.add_layout(Legend(), 'above')
    pSES.line(x='dt_form', y='mean_sengine_score', color='#0600b3', alpha=0.5,
                line_width = LINE_W, legend_label=f'Mean score {seng}', source=cdsQC)
    pSES.yaxis.axis_label = 'Search Engine Score'
    add_repeated_elements(pSES)
    
    tooltips = [('File', '@raw_file'), ('PSMs', '@psm_number')]
    pRTs = figure(plot_width=eachWidth*2, plot_height=EACH_HEIGHT,
                  x_axis_type='datetime',
                  x_range=pQCPSM.x_range, tools=commonToolstring,
                  active_drag='box_zoom', toolbar_location='right', tooltips=tooltips)
    pRTs.add_layout(Legend(), 'right')
    for pLab, pColor in (('pept_416', '#005566'),('pept_425', '#005566'), ('pept_488', '#00635b'),
                         ('pept_495', '#006344'), ('pept_567', '#006324'),
                         ('pept_652', '#006607'), ('pept_655', '#2c9403')):
        pRTs.line(x='dt_form', y=pLab, color=pColor, alpha=0.5,
                    line_width = LINE_W, legend_label=pLab, source=cdsQC)
    pRTs.yaxis.axis_label = 'Retention time, min'
    pRTs.min_border_top = 30
    add_repeated_elements(pRTs)
    
    #Service display bar
    servD = figure(plot_width=full_width, plot_height=SERVD_HEIGHT,
                   x_axis_type='datetime', x_range=pQCPSM.x_range,
                   tools='xwheel_zoom,xpan,reset,save', active_scroll='xwheel_zoom',
                   toolbar_location='below')
    servD.add_tools(HoverTool(
        tooltips=[( 'Procedure',   '@type' ),
                  ( 'Date',   '@dt_form{%F}' ) ],
        formatters={'@dt_form': 'datetime'} ) )
    servD.border_fill_color = PLOT_BGR_COL
    servD.background_fill_color = PLOT_BGR_COL
    servD.xaxis.major_label_text_color = 'white'
    servD.yaxis.major_label_text_color = PLOT_BGR_COL
    servD.xaxis.axis_line_width = 0
    servD.xaxis.major_tick_line_color = None
    servD.yaxis.axis_line_width = 0
    servD.yaxis.major_tick_line_color = None
    servD.yaxis.minor_tick_line_color = None
    servD.ygrid.grid_line_color = None
    servD.vbar(x='dt_form', bottom=0, top=1, color='#ff9100', width=700_000_000, source=cdsServ)
    servD.title.text = 'Service/Cleaning:'
    servD.title.align = 'left'
    servD.title.text_color = 'white'
    servD.title.text_font_size = '14px'
    servD.title.text_font_style = 'normal'

    return servD, pQCPSM, pIdMsms, pInjTimes, pMzErr, pMzErrStd, pPWidth, pAbund, pSES, pRTs

def qcplots_global(cdsQC, full_width=1000, seng='Mascot'):
    eachWidth = int(full_width / 2)
    EACH_HEIGHT = 350
    
    txtPSc = Div(text='General relationships between variables:', margin=(20,10,10,10),
                     width=full_width)
    txtPSc.style = {'width': f'{full_width}px',
                        'font-size': '20px', 
                        'box-sizing': 'border-box'
                        }
    
    tooltips = [('File', '@raw_file'), ('PSMs', '@psm_number'), (f'Mean score {seng}', '@mean_sengine_score')]
    pSc1 = figure(plot_width=eachWidth, plot_height=EACH_HEIGHT,
                  tools='box_zoom,wheel_zoom,pan,reset,save', active_drag='box_zoom',
                  toolbar_location='right', tooltips=tooltips)
    pSc1.circle(x='mean_sengine_score', y='psm_number', color='navy', alpha=0.4, size = 4, source=cdsQC)
    pSc1.xaxis.axis_label = f'Mean score {seng}'
    pSc1.yaxis.axis_label = 'PSMs'
    def add_repeated_elements(plotObj):
        plotObj.border_fill_color = '#e8e8ed'
        plotObj.min_border_left = 80
        plotObj.min_border_right = 50
        plotObj.min_border_top = 30
        plotObj.min_border_bottom = 50
        plotObj.background_fill_color = '#e8e8ed'
        plotObj.xaxis.axis_label_text_font_size = '16px'
        plotObj.yaxis.axis_label_text_font_size = '16px'
        plotObj.xaxis.major_label_text_font_size = '12px'
        plotObj.yaxis.major_label_text_font_size = '12px'
    add_repeated_elements(pSc1)


    tooltips = [('File', '@raw_file'), ('PSMs', '@psm_number'), ('Mean peak width, s', '@mean_peak_width')]
    pSc2 = figure(plot_width=eachWidth, plot_height=EACH_HEIGHT,
                  tools='box_zoom,wheel_zoom,pan,reset,save', active_drag='box_zoom',
                  toolbar_location='right', tooltips=tooltips)
    pSc2.circle(x='mean_peak_width', y='psm_number', color='#7a00b8', alpha=0.4, size = 4, source=cdsQC)
    pSc2.xaxis.axis_label = 'Mean peak width, s'
    pSc2.yaxis.axis_label = 'PSMs'
    add_repeated_elements(pSc2)
    
    return txtPSc, pSc1, pSc2

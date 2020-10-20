# bokehQCDashboard
QC dashboard for proteomics using python and bokeh

Created and tested by Egor Vorontsov.

The dashboard makes use of the key QC values that are stored in an SQLite database. During the development of the dashboard, the QC runs were injections of 50 ng of a HeLa cell tryptic digest, and the database is filled with the output values from Proteome Discoverer 2.4 searches that are processed via the "QC_Script_PD2.4" Python script.

The file templates/index.html is added in order to change the background color of the app.

The app consists of one long page and is based on bokeh library:

<img src="https://github.com/dev-ev/bokehQCDashboard/blob/main/bokehQC_screenshot_1.PNG" alt="drawing" width="400"/>

Select the instrument using the dropdown menu on the left:

<img src="https://github.com/dev-ev/bokehQCDashboard/blob/main/bokehQC_screenshot_2.PNG" alt="drawing" width="200"/>


Hover over a bar on the "Service/Cleaning" plot to see the details about the procedure:

<img src="https://github.com/dev-ev/bokehQCDashboard/blob/main/bokehQC_screenshot_3.PNG" alt="drawing" width="600"/>

By default, the app displays the data for the whole time that is available in the database. Zoom in onto a plot to see a smaller region on both axes:

<img src="https://github.com/dev-ev/bokehQCDashboard/blob/main/bokehQC_screenshot_4.PNG" alt="drawing" width="400"/>

The time span on all the plots will change in sync:

<img src="https://github.com/dev-ev/bokehQCDashboard/blob/main/bokehQC_screenshot_5.PNG" alt="drawing" width="400"/>

Hover over a point on a plot to see the numbers:

<img src="https://github.com/dev-ev/bokehQCDashboard/blob/main/bokehQC_screenshot_6.PNG" alt="drawing" width="300"/>

The main QC table contains the following columns:

search_id INTEGER PRIMARY KEY,
raw_file TEXT NOT NULL,
file_date TEXT,
search_date TEXT,
instrument TEXT,
protein_number INTEGER,
peptide_number INTEGER NOT NULL,
psm_number INTEGER NOT NULL,
msms_number INTEGER NOT NULL,
id_rate REAL,
mean_psm_it_ms REAL,
median_psm_it_ms REAL,
mean_msms_it_ms REAL,
median_msms_it_ms REAL,
mean_mz_err_ppm REAL,
median_mz_err_ppm REAL,
mz_err_ppm_stdev REAL,
total_prec_intensity REAL,
mean_prec_intensity REAL,
mean_sengine_score REAL,
mean_peak_width REAL,
peak_width_stdev REAL,
pept_416 REAL,
pept_425 REAL,
pept_488 REAL,
pept_495 REAL,
pept_567 REAL,
pept_652 REAL,
pept_655 REAL,
comment TEXT

The "service" table contains the following columns:

procedure_id INTEGER PRIMARY KEY,
date TEXT NOT NULL,
type TEXT,
is_pm TEXT,
comment TEXT

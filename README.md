# bokeh-QC-dashboard
QC dashboard for proteomics using python and bokeh Created and tested with Orbitrap mass spectrometers in mind.

The dashboard makes use of the key QC values that are stored in an SQLite database. During the development of the dashboard, the QC runs were injections of 50 ng of a HeLa cell tryptic digest, and the database is filled with the output values from Proteome Discoverer 2.4 searches that are summarized and saved into an SQLite database by [the integrated *QC_Script_PD2.4*](https://github.com/dev-ev/qc-script-PD24) script.

The file templates/index.html is added in order to change the background color of the app.

The app consists of one long page and is based on bokeh library:

<img src="https://github.com/dev-ev/bokehQCDashboard/blob/main/screenshots/bokehQC_screenshot_1.PNG" alt="drawing" width="400"/>

Select the instrument using the dropdown menu on the left:

<img src="https://github.com/dev-ev/bokehQCDashboard/blob/main/screenshots/bokehQC_screenshot_2.PNG" alt="drawing" width="200"/>


Hover over a bar on the "Service/Cleaning" plot to see the details about the procedure:

<img src="https://github.com/dev-ev/bokehQCDashboard/blob/main/screenshots/bokehQC_screenshot_3.PNG" alt="drawing" width="600"/>

By default, the app displays the data for the whole time that is available in the database. Zoom in onto a plot to see a smaller region on both axes:

<img src="https://github.com/dev-ev/bokehQCDashboard/blob/main/screenshots/bokehQC_screenshot_4.PNG" alt="drawing" width="400"/>

The time span on all the plots will change in sync:

<img src="https://github.com/dev-ev/bokehQCDashboard/blob/main/screenshots/bokehQC_screenshot_5.PNG" alt="drawing" width="400"/>

Hover over a point on a plot to see the numbers:

<img src="https://github.com/dev-ev/bokehQCDashboard/blob/main/screenshots/bokehQC_screenshot_6.PNG" alt="drawing" width="300"/>



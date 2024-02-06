# A-plugin-for-variable-frequency-pump-settings-in-PySWMM
A plugin for variable frequency pump settings in PySWMM, primarily addressing the issue of PySWMM's inability to set variable frequency operations for pumps over time, as well as the issue with SWMM-API's inability to use hot start files. This plugin integrates two open-source libraries to implement variable frequency settings for pumps. Additionally, it utilizes the Plotly library to visualize the time series results outputted by SWMM.

"Main_Use.py" is used for execution, where "read_out.py" and "swmm_code.py" are respectively for reading the .out files and running the underlying framework for SWMM simulation. The file "curve.csv" contains the time series data for pump operation schedules. "v1.inp" is the SWMM framework model for the experimental site. The SWMM's inp, out, hsf, and rpt files are used to save the SWMM input, output, hot start, and report files for each time period, respectively.

P.S:
You can change you own "curve.csv" for you pumps and "v1.inp" for you own SWMM model, and you need to change code in "swmm_code.py" to match and read each column from the CSV with the pumps in the SWMM model and change the inputs of "data" and "in_file" within the function "swmm_run" in "Main_Use.py"

You can adjust the "time_set", "step_hour", and "time_step" variables to respectively correspond to the start time of the model simulation, the interval time for pump changes, and the simulation step length for each phase. However, it is important to note that the modified pump change interval time should match the time interval found in the imported pump frequency data CSV file.

In order to select which nodes or links to focus on, you can modify the inputs of "nodes" and "links" within the "read_out" function in "Main_Use.py" to correspond to the node and link IDs you wish to view.

Overall code execution time:
If running both the swmm_run + read_out sections in "Main_Use" (i.e., simulation + Plotly display), it takes a total of 85.826 minutes.
If only executing the read_out display (by commenting out the swmm_out), it requires 83.300 seconds.

# Repository Structure

`Simple Bioprocess Monitor/`: Project creates a simple, reusable "bioprocess monitor" class to help visualize bioprocess data.

`overview/`: The goal of this project was to create a basic visualization tool for batch bioprocess data. Data from a .csv file can be represented and have simple analyses performed on it using the code. Specifically, the code was centered around interpretting bioprocess data as an example. The project also gave me the opportunity to familiarize myself with data visalisation in Python for the first time.

`Features/`: 
-Compares/filters pH and temperature data to user-specified limits
-Plots various concentration data as a function of time
-Generates visual dashboard with plots to represent the aformentionned information on the data set
-Creates a summary table with summary entries for data on a per-batch basis.

`technnologies/`: Following tools were used to create the project :
-Python 3.14.7 for the main programming language
-Matplot 3.0.5 for data plotting/visualization
-Pandas 3.11.0 for data extraction


`code design/`: When main.py runs, it uses the "BioprocessMonitor" class to compare the data for each of the 5 batches to 2 different sets of temperature and pH limits. Each batch has 2 dashboards generated for it, one for both combinations of T/pH limits. Then, 2 summary tables, one for each set of limits, is generated. 

`dashboard/`: 
Example dashboard for batch #5 data with pH[] and temperature[] limits.
<img width="2560" height="1920" alt="Batch_005_Mode_B" src="https://github.com/user-attachments/assets/9b38e970-1e16-4e31-a149-6d2a3c13795e" />

`summary table/`: 
Summary data for each paramater for all batches and pH[] and temperature[] limits.

|batch_id|ph_optimal_percent|temperature_optimal_percent|C_product_g_L^-1_final|
|--------|------------------|---------------------------|----------------------|
|1       |36.08             |51.55                      |46.5                  |
|2       |34.71             |55.37                      |50.8                  |
|3       |36.99             |46.58                      |44.6                  |
|4       |54.12             |62.35                      |48.6                  |
|5       |16.51             |49.54                      |24.7                  |



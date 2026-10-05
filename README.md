# Repository Structure

`Simple Bioprocess Monitor/`: Project creates a simple, reusable "bioprocess monitor" class to help visualize bioprocess data.

`overview/`: The goal of this project was to create a basic visualization tool for batch bioprocess data. Data from a .csv file can be represented and have simple analyses performed on it using the code. Specifically, the code was centered around interpretting bioprocess data as an example. The project also gave me the opportunity to familiarize myself with data visalisation in Python for the first time.

`Features/`: 
-Compares/filters pH and temperature data to user-specified limits
-Plots various concentration data as a function of time
-Generates visual dashboard with plots to represent the aformentionned information on the data set
-Creates a summary table with summary entries for data on a per-batch basis.

`technnologies/`: Following tools were used to create the project :
-Python
-Matplot
-Pandas
-Numpy

`.gitignore`: Contains files to be ignored by Git. You can copy the `.gitignore` file from this repository into your own
project.

`environment.yaml`: Contains information about your conda environment. Run the following command:
`conda export > environment.yaml` to generate this file for your project. You can delete the last line in this file that
says `prefix`.

`main.py`: This is the only Python file that will be run. It should be kept relatively clean and mainly execute code
from `src/`.

`README.md`: This file, which contains information about the repository.

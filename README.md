# fsri-compartments-2018
This repository contains data from compartment fire experiments that were conducted as part of a project that examined the use of fire dynamics analysis techniques with furniture-fueled fires. Information about the experiments and a Python script that generates charts of the experimental data are also included in this repository.

This project was supported by Award No. 2017-DN-BX-O163, awarded by the National Institute of Justice, Office of Justice Programs, U.S. Department of Justice. The opinions, findings, and conclusions or recommendations expressed in this publication/program/exhibition are those of the author(s) and do not necessarily reflect those of the Department of Justice.

## 01_Data
The data directory includes one data file and one events file for each experiment. More information about the file structures and the corresponding experiments can be found here: [01_Data/README.md](01_Data/README.md)

## 02_Info
The info directory contains a plaintext __.csv__ channel list that is referenced by the plotting script to properly map data channels to their respective sensor groups, add labels to the chart legends, and assign the file names of the charts that are generated. Additional information about the instrumentation including a dimensioned floor plan of sensor locations can be found here: [02_Info/README.md](02_Info/README.md)

## 03_Scripts
A single Python script, __plot.py__, is included in the scripts directory. When executed, the script generates __.pdf__ graphs that contain data plots from each sensor group for every experiment. In conjunction with Matplotlib, Seaborn is used to style the graph. If seaborn is not already installed, it can be added by the following:
```
pip install seaborn
```
If you are using the Anaconda distribution of python, it can alternatively be installed by:
```
conda install seaborn
```

## 04_Charts
The chart directory is produced upon execution of __plot.py__. The charts produced by the Python script are saved in subdirectories that correspond to each compartment fire experiment. Because the graphs can be produced from files included in this repository, the graphs themselves are not files under version control.

###
For more information about the project, [Contact Us](https://fsri.org/contact-fire-safety-research-institute).

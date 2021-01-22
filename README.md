# Inorganic geochemistry QA program

## Description of program
This program is a QA/QC program used to compare the original and uploaded inorganic geochemistry data from Geoscience Australia to make sure uploaded results are accurate. 

## Requirements
This program requires the Pandas Python library and all of its associated requirements.
To install use **pip install Pandas** in either the command prompt or depending on your IDE can be done in the terminal of the open project.

The when downloading the excel sheets of the uploaded data it should be downloaded with each technique per line.

## Using the program
When running the program copy the path of the uploaded data excel file first and paste when prompted, then copy the path of the original data sheet when prompted.
Only requires further input to either continue or quit the program.

## Current bugs
1. When creating a data frame for ICPMS data on some excel sheets it will use the incorrect columns.
   This will occur mostly in ICPMS sheets with an extra column called comments, the program will sometimes inaccurately not identify this.
2. When doing comparisons between the data if it is considered wrong the message that says which piece of data is wrong will not always be printed.


#!/bin/bash
rm -rf venv
python -m venv venv
. venv/bin/activate

# Check dependencies
pip install biopython
pip install matplotlib
pip install flask
pip install flask-wtf
pip install flask-bootstrap4
pip install flask-sqlalchemy

# Read excel files
pip install xlrd
pip install openpyxl
pip install pandas
pip install xlrd

# Download data
wget http://datazone.birdlife.org/userfiles/file/Species/Taxonomy/HBW-BirdLife_Checklist_v3_Nov18.zip
unzip HBW-BirdLife_Checklist_v3_Nov18.zip -d static/data/
rm HBW-BirdLife_Checklist_v3_Nov18.zip

# Process data

#linkpath = 'http://datazone.birdlife.org/species/factsheet/'

#python CreateCSV.py
#python readCSV.py

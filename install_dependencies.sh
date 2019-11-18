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

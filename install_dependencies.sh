#!/bin/bash
#pip3 install virtualenv
rm -rf venv
#python -m virtualenv venv
python3 -m venv venv
. venv/bin/activate

# Check dependencies
pip3 install biopython
pip3 install matplotlib
pip3 install flask
pip3 install flask-wtf
pip3 install flask-bootstrap4
pip3 install networkx
#pip3 install pygraphviz
pip3 install pydot
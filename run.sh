#!/bin/bash
. venv/bin/activate

export FLASK_APP=app_run.py
export FLASK_ENV=development
#python $FLASK_APP
flask run

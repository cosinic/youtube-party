#!/bin/bash

export FLASK_APP=src/__init__.py
PORT=8080

if [ "$1" != "" ]; then 
  PORT=$1
fi

flask run --host=0.0.0.0 --port=$PORT

#!/bin/bash

python3 -m venv venv/lg
source venv/lg/bin/activate && pip install -U pip --quiet && pip install langgraph langsmith
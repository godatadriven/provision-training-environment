#!/bin/bash

source /anaconda/bin/activate {{ item.env }}

export PATH=/anaconda/envs/{{ item.env }}/bin:$PATH

exec /anaconda/envs/{{ item.env }}/bin/jupyter notebook --config /home/{{ item.name }}/.jupyter/jupyter_notebook_config.py &> /dev/null &
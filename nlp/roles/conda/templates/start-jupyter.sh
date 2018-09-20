#!/bin/bash

source /miniconda/bin/activate {{ item.env }}

export PATH=/miniconda/envs/{{ item.env }}/bin:$PATH

exec /miniconda/envs/{{ item.env }}/bin/jupyter notebook --config /miniconda/envs/{{ item.env }}/.jupyter/jupyter_notebook_config.py &> /dev/null &
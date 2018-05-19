#!/bin/bash

source /miniconda/bin/activate {{ conda_environment_name }}

export PATH=/miniconda/envs/{{ conda_environment_name }}/bin:$PATH

exec /miniconda/envs/{{ conda_environment_name }}/bin/jupyter notebook --config /miniconda/envs/{{ conda_environment_name }}/.jupyter/jupyter_notebook_config.py &> /dev/null &
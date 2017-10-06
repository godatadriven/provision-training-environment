#!/bin/bash

source /etc/spark2/conf/spark-env.sh

export PATH=/anaconda/bin:$PATH
export PYSPARK_PYTHON=/anaconda/bin/python

exec /anaconda/bin/jupyter notebook &> /dev/null &
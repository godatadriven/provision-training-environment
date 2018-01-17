#!/bin/bash

if [ ! -f ds-spark-data.zip ]; then
  wget --no-check-certificate https://misc-godatadriven.s3.amazonaws.com/ds-spark-data.zip
  unzip ds-spark-data.zip
fi

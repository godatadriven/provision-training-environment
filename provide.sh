#!/bin/bash
set -e

usage="$(basename "$0") [-h] [-i PROJECT] [-n WORKERS] [-p PYTHON] [-d NOTEBOOKS_DIR]

Make a user provide SSH key and jupyter notebooks (in roles/bootstrap/files/notebooks) to each user listed in var/common.yml

where:
    -h  show this help text
    -i  google cloud project id
    -v  number of workers
    -p  python path
    -d  the notebooks dir you want to copy"

# constants
PYTHON=python3
NOTEBOOK_DIR=false

options=':hi:v:p:d:'
while getopts $options option; do
  case "$option" in
    h) echo "$usage"; exit;;
    i) PROJECT=$OPTARG;;
    n) WORKERS=$OPTARG;;
    p) PYTHON=$OPTARG;;
    d) NOTEBOOK_DIR=$OPTARG;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2; echo "$usage" >&2; exit 1;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2; echo "$usage" >&2; exit 1;;
  esac
done

if [ ! "$PROJECT" ]; then
  echo "argument -i must be provided"
  echo "$usage" >&2; exit 1
fi


# if copying notebooks to the instance
if $NOTEBOOK_DIR; then
  cp -aR $NOTEBOOKS_DIR roles/bootstrap/files/notebooks
fi

virtualenv provision_env -p $PYTHON
source provision_env/bin/activate
pip install delegator.py pyyaml ansible click
python deploy.py --workers=$WORKERS --project=$PROJECT_ID
ansible-playbook -i hosts --private-key gcloud_ansible playbook.yml

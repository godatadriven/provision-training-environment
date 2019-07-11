# Provision training environment

This is the repository to provision the training environment for the NLP with Deep Learning training.

## Prerequisites

You need to have the [gcloud CLI](https://cloud.google.com/sdk/downloads) installed.
You need to be authenticated (`gcloud auth login`) and to have chosen the correct Google Cloud project (`gcloud config set project <project_id>`).
Note: make sure to use the `project_id` and not the `project_name`.

You need a Python 3 interpreter and install the following packages (`pip` suffices):

- `click`
- `delegator.py` (note: don't use `pip install delegator`)
- `pyyaml`
- `ansible`


## Usage

Remember to put the

- The list of users into `var/common.yml`, under `users`;
- The tarballed course materials directory, including data, at `https://storage.googleapis.com/godatadriven-academy-trainings-data/nlp-with-dl.tar.gz`.

Then execute:

```bash
export PROJECT_ID=my-project  # you can skip it if it's configured in your gcloud default values
python deploy-nlp-with-dl.py --instances <num_instances> [optional: --name <name-prefix>] 
ansible-playbook -i nlp-hosts --private-key gcloud_nlp_ansible playbook-nlp-with-dl.yml
```

You should be good to go now!

## Access

To SSH into the machine and set up port forwarding:

```bash
ssh -i gcloud_ansible -o IdentitiesOnly=yes <my_user>@<instance_external_ip>
```

The `instance_external_ip` can be found in the `nlp-with-dl-hosts` file.

Ports 5000 and 6006-6010 are opened up to access jupyter and tensorboard.

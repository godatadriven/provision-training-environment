# Provision training environment

This is the repository to provision the training environment for the NLP training.

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
- The notebooks in `roles/conda/files/notebooks`

Be aware that the ansible script expects one of the folders you save in `roles/conda/files/notebooks` to be called `exercises/`; the script will set a subdirectory called `data/` with all of the necessary files in `exercises/`. 

Then execute:

```bash
export PROJECT_ID=my-project  # you can skip it if it's configured in your gcloud default values
python deploy-elastic.py --instances <num_instances> [optional: --name <name-prefix>] 
ansible-playbook -i elastic-hosts --private-key gcloud_elastic_ansible playbook-elastic.yml
```

You should be good to go now!

## Access

To SSH into the machine and set up port forwarding:

```bash
ssh -i gcloud_ansible -o IdentitiesOnly=yes <my_user>@<instance_external_ip>
```

The `instance_external_ip` can be found in the `elastic-hosts` file.

Ports 9200, 5601, and 5000 are opened up to access Elasticsearch, Kibana, and Jupyter, respectively, and ports 10000 and 5044 are opened for internal use by Netcat and Filebeat.

Be aware that only the Wibaut IP address is whitelisted in the firewall settings! To give this training in another location (or to access the GCEs from home, say), after creating your GCEs do the following in the Google Cloud Console:

+ navigate to `VPC Network` -> `Firewall rules`
+ click on `allow-elastic-training-ports`
+ click on `Edit`
+ add the desired IP address under `Source IP ranges`
+ click on `Save`

Be aware that the following time you run `deploy-elastic.py`, these added IP addresses will be removed.  
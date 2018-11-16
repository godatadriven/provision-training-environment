# Provision training environment

This is the repository to provision the training environment for the Data Science with Spark
training.

We are currently in the process of making it grow to become more robust and serve more targets
(possibly with Anaconda installed).


## Prerequisites

You need to have the [gcloud CLI](https://cloud.google.com/sdk/downloads) installed.
First authenticate and set the correct Google Cloud project. If you don't know your `project_id`, go to console.cloud.google.com and look for a project with trainings among your projects. Make sure you are logged on with your `@godatadriven.com` e-mail. Note: make sure to use the `project_id` and not the `project_name`.

> Normally we use project_id `trainings-166610` (name: `trainings`) part of the organisation GoDataDriven. An admin (Gio
 or Kris) can invite you. 

```bash
gcloud auth login
gcloud config set project <project_id>
```

Install the local environment and activate it

```
conda env create -f environment.yml
source activate provision-training-environment
```

## Usage

Remember to put the

- The list of users into `var/common.yml`, under `users`;
- The notebooks in `roles/bootstrap/files/notebooks`.

You don't have to do this for a test run though. Then execute:

```bash
# you might need to configure your shell for unicode settings in Python 3:
export LC_ALL=en_US.UTF-8

python deploy.py --workers <num_workers> [optional: --name <cluster-name>] # this will print out the master IP to the console
ansible-playbook --private-key gcloud_ansible playbook.yml
```

You should be good to go now!

The master IP is written to `host` and all previous content is discarded.
To provision older clusters, keep your IPs somewhere separate.


## Access

To SSH into the machine and set up port forwarding:

```bash
ssh -i gcloud_ansible -o IdentitiesOnly=yes -L <port>:localhost:<port> <my_user>@<master_external_ip>
```

The `master_external_ip` can be found in the `hosts` file.

Now use the same port to start a Jupyter Notebook server on the Gateway:

```bash
jupyter notebook --port <port>
```

Distribute the key to your users, and they should also be able to log in.

Note: This is not for a secure environment, where everybody has their own key.
However, as all users have sudo privileges anyway, that doesn't really matter.

## Teardown
When you are done, remove your cluster manually here:
https://console.cloud.google.com/dataproc/clusters

```bash
# Find running cluster(s):
gcloud dataproc clusters list --region europe-west1

# Remove running cluster
gcloud dataproc clusters delete --region europe-west1 cluster-******** 
```

## Testing

If you have docker, be sure to have `localhost` as master in your `hosts`.
Then run:

```
docker build -t gcloud_ansible .
```

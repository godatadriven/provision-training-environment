# Provision training environment

This is the repository to provision the training environment for the Data Science with Spark
training.

We are currently in the process of making it grow to become more robust and serve more targets
(possibly with Anaconda installed).


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
- The notebooks in `roles/bootstrap/files/notebooks`.

Then execute:

```bash
export PROJECT_ID=my-project  # you can skip it if it's configured in your gcloud default values
python deploy.py --workers <num_workers> [optional: --name <cluster-name>] # this will print out the master IP to the console
ansible-playbook -i hosts --private-key gcloud_ansible playbook.yml
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


## Testing

If you have docker, be sure to have `localhost` as master in your `hosts`.
Then run:

```
docker build -t gcloud_ansible .
```

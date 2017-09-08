# Provision training environment

This is the repository to provision the training environment for the Data Science with Spark
training.

We are currently in the process of making it grow to become more robust and serve more targets
(possibly with Anaconda installed).

## Prerequisites

You need to have the gcloud CLI installed. You need to authenticated and to have chosen the correct
Google Cloud project (`gcloud config set project <project_id>`). Make sure to use the `project_id` and not the `project_name`.

You need to install the `delegator` package https://github.com/kennethreitz/delegator.py 
Note: 2017-06-19 `pip install delegator` did not work for me, installs version 0.0.3 You need to use `pip install delegator.py`

You need to install `pyyaml`. `pip install pyyaml`
Note: 2017-06-19 `pip install yaml` installation works but breaks when running the code.

You need to install ansible
Note: 2017-06-19 in Ubuntu `sudo apt-get install ansible`, On your mac just do `pip install ansible boto3`

## Usage

Once you have create your cluster, you need three things:

- The VM name (f.e. `cluster-1-m`);
- The list of users (put them into `var/common.yml`, under `users`);
- The notebooks you want to upload stored in `roles/bootstrap/files/notebooks`.

Then execute

```
python deploy.py <vm_name>
ansible-playbook -i hosts --private-key gcloud_ansible playbook.yml
```

You should be good to go now!

```
ssh -i gcloud_ansible -o IdentitiesOnly=yes -L <port>:localhost:<port> <my_user>@<master_external_ip>
jupyter notebook --port <port>
```

The `master_external_ip` can be found in the `hosts` file.

Distribute the key to your users, and they should also be able to log in.



NOTE: This is not for a secure environment, where everybody has their own key. However, as all users
have sudo privileges anyway, that doesn't really matter.


## Testing

If you have docker, be sure to have `localhost` as master in your `hosts`. Then

```
docker build -t gcloud_ansible .
```

#!/bin/env python
import os
import sys
import random
import logging

import delegator
import yaml
import click

KEY_PATH = "gcloud_ansible"
KEYS_PATH = 'keys'
YAML_PATH = "vars/common.yml"
HOSTS_PATH = 'hosts'

class GCloudError(Exception):
    def __init__(self, message):
        super().__init__(message)

def create_key_pair(key_path):
    if not os.path.isfile(key_path):
        delegator.run('ssh-keygen -b 2048 -t rsa -f %s -q -N ""' % key_path)


def load_yml(path):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    return data


def load_key(path):
    with open(path + ".pub", 'r') as f:
        key = f.read()
    return key


def write_users(yml, key, key_path):
    with open(key_path, 'w') as f:
        for user in yml.get('users', []) + [yml.get('deployer')]:
            f.write(''.join([user, ':', key]))


def add_keys_to(instance_tag, key_path, zone):
    # TODO This method could be optional
    delegator.run(("gcloud compute instances add-metadata %s "
                   "--zone=%s --metadata-from-file sshKeys=%s") % (instance_tag, zone, key_path))

def get_ip_of(instance_tag):
    # TODO This method could be optional
    c = delegator.run(('gcloud --format="value(networkInterfaces[0].accessConfigs[0].natIP)" '
                       'compute instances list --filter="name=(%s)"') % instance_tag)
    external_ip = c.out.strip()
    if c.err:
        raise GCloudError(c.err)
    elif not external_ip:
        raise GCloudError("No external ip found for instance {}"
                          .format(instance_tag))

    print("external ip found for instance {}: {}"
          .format(instance_tag, external_ip))
    return external_ip


def zone_of(instance_tag):
    c = delegator.run(('gcloud --format="value(zone)" '
                       'compute instances list %s') % instance_tag)
    zone = c.out.strip()
    return zone


def write_ip_to(hosts_path, external_ip):
    with open(hosts_path, 'w') as f:
        f.write('[master]')
        f.write('\n')
        f.write(external_ip)
        f.write('\n')


def get_variables():
    return (os.environ.get('KEY_PATH', KEY_PATH),
            os.environ.get('KEYS_PATH', KEYS_PATH),
            YAML_PATH,
            HOSTS_PATH)


def get_random_id(N_sequence):
    _id = ''
    numbers = list(range(10))
    for _ in range(N_sequence):
        _id += str(random.choice(numbers))
    return _id

def get_cluster_name(name, N_sequence=10):
    if name:
        return f"cluster-{name}"
    else:
        return f"cluster-{get_random_id(N_sequence)}"


def create_cluster(project_id, cluster_name, workers, bucket, single):
    to_run = f"""gcloud dataproc --region europe-west1 clusters create {cluster_name}
    --subnet default --zone europe-west1-c
    --master-machine-type n1-standard-16 --master-boot-disk-size 100
    --initialization-actions 'gs://gdd-trainings-bucket/install_conda.sh'
    """
    if project_id:
        to_run += f" --project {project_id}"
    if bucket:
        to_run += f" --bucket {bucket}"
    if not single:
        to_run += f"--num-workers {workers} --worker-machine-type n1-standard-4 --worker-boot-disk-size 100"
    else:
        to_run += f"--single-node"
    c = delegator.run(to_run.replace('\n', ' '))
    if c.err:
# don't raise, it's printing to standard error but it's not an error
        logging.warning(c.err)


@click.command()
@click.option('--project', default=None, help="Google project")
@click.option('--workers', default=3, help="Number of workers")
@click.option('--name', default=None, help="Google Dataproc Clustername")
@click.option('--bucket', default=None, help="Bucket to mount")
@click.option('--single-node', default=None, help='Single instance')
def main(project, workers, name, bucket, single_node):
    cluster_name = get_cluster_name(name)
    create_cluster(project, cluster_name, workers, bucket, single_node)
    instance_tag = f"{cluster_name}-m"
    key_path, keys_path, yaml_path, hosts_path = get_variables()
    create_key_pair(key_path)
    yml = load_yml(yaml_path)
    key = load_key(key_path)
    write_users(yml, key, keys_path)
    zone = zone_of(instance_tag)
    add_keys_to(instance_tag, keys_path, zone)
    external_ip = get_ip_of(instance_tag)
    write_ip_to(hosts_path, external_ip)

if __name__ == "__main__":
    main()

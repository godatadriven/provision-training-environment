#!/bin/env python
import os
import sys
import random
import logging

import delegator
import yaml
import click

KEY_PATH = "gcloud_elastic_ansible"
KEYS_PATH = 'elastic-keys'
YAML_PATH = "vars/common.yml"
HOSTS_PATH = 'elastic-hosts'

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

def add_firewall_rules():
    delegator.run("gcloud compute firewall-rules delete allow-elastic-training-ports ")
    delegator.run(r"""gcloud compute firewall-rules create allow-elastic-training-ports \
                   --allow tcp:9200,tcp:5601,tcp:5000,tcp:10000 \
                   --source-ranges 37.17.221.89/32 \
                   --target-tags elastic-training-instance \
                   --description 'Allow access to Elasticsearch, Kibana, Logstash, Netcat and Jupyter'""")

def init_host_file(hosts_path):
    with open(hosts_path, 'w') as f:
        f.write('[elastic-instances]')
        f.write('\n')

def write_ip_to(hosts_path, external_ip):
    with open(hosts_path, 'a') as f:
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

def get_instance_name_prefix(name, N_sequence=10):
    if name:
        return f"elastic-{name}"
    else:
        return f"elastic-{get_random_id(N_sequence)}"


def create_machines(project_id, name_prefix, instances):
    # to_run = f"""gcloud dataproc --region europe-west1 clusters create {cluster_name}
    # --subnet default --zone europe-west1-c
    # --master-machine-type n1-standard-16 --master-boot-disk-size 100 --num-workers {workers}
    # --worker-machine-type n1-standard-4 --worker-boot-disk-size 100
    # --initialization-actions 'gs://gdd-trainings-bucket/install_conda.sh'
    # """
    for instance in range(0,instances):
    	machine_name = f"{name_prefix}-{instance}"
    	to_run = f"""gcloud beta compute instances create {machine_name} 
    	--subnet=default --zone=europe-west1-c
    	--machine-type=n1-standard-4
    	--tags elastic-training-instance
    	--boot-disk-size=20GB --boot-disk-type=pd-standard --boot-disk-device-name={machine_name}
		"""
    	# --network-tier=PREMIUM
    	# --maintenance-policy=MIGRATE
    	# --service-account=787238606102-compute@developer.gserviceaccount.com
    	# --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append
    	# --tags=http-server,https-server
    	# --image=debian-9-stretch-v20180510
    	# --image-project=debian-cloud 
    	if project_id:
        	to_run += f" --project_id {project_id}"
    	c = delegator.run(to_run.replace('\n', ' '))
    	if c.err:
			# don't raise, it's printing to standard error but it's not an error
        	logging.warning(c.err)


@click.command()
@click.option('--project', default=None, help="Google project")
@click.option('--instances', default=3, help="Number of instances")
@click.option('--name', default=None, help="Google instancename prefix")
def main(project, instances, name):
    name_prefix = get_instance_name_prefix(name)
    create_machines(project, name_prefix, instances)
    add_firewall_rules()
    key_path, keys_path, yaml_path, hosts_path = get_variables()
    create_key_pair(key_path)
    yml = load_yml(yaml_path)
    key = load_key(key_path)
    write_users(yml, key, keys_path)
    init_host_file(hosts_path)
    for instance in range(0, instances):
    	instance_tag = f"{name_prefix}-{instance}"
    	zone = zone_of(instance_tag)
    	add_keys_to(instance_tag, keys_path, zone)
    	external_ip = get_ip_of(instance_tag)
    	write_ip_to(hosts_path, external_ip)

if __name__ == "__main__":
    main()

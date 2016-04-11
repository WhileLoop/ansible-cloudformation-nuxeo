# Introduction

This is a proof of concept implementation of a deployment method in which Ansible and Cloudformation are used to provision and configure all AWS resources and servers, and dynamically 'wire' all components together. A Cloudformation stack is deployed and all values that are needed to connect various component are saved as Cloudformation outputs. When configuring the servers, Ansible queries these values and templates them into the appropriate configuration files.

### Overview

A simple stack consisting of one webserver instance running the Nuxeo document managment application, and another instance with a dedicated database is provisioned. Cloudformation saves the hostname of the database, and the IP address of the webserver. When configuring the servers, Ansible queries these values and the database hostname is templated into the Nuxeo configuration file so the webserver application knows where the database is. The IP address of the webserver is templated by Ansible into the PostgreSQL pg_hba.conf file in order for the database to allow access from the webserver.

# Getting Started Locally

To test the roles locally simply run 'vagrant up'. This will install Ansible on a Ubuntu VM and run the playbook locally with the following command: `ansible-playbook configure_servers.yml --extra-vars '@variables/local.yml' -i 'localhost,' --connection local`. Point your browser to localhost:8080 to access the application. Default credentials are 'Administrator/Administrator'.

# Deplyoing to AWS

First configure the Ansible EC2 dynamic inventory (http://docs.ansible.com/ansible/intro_dynamic_inventory.html#example-aws-ec2-external-inventory-script). At the very minimum you will need to set the proper credentials for Boto to query your AWS account, and set the appropriate AWS regions in ec2.ini, and make ec2.py executable.

export AWS_ACCESS_KEY_ID=[ ACCESS KEY ]
export AWS_SECRET_ACCESS_KEY=[ SECRET_KEY ]
chmod +x inventory/ec2.py

Next, in the file variables/aws.yml you need to set the aws_access_key, and aws_secret_key variables. These are used by the Ansible Cloudformation module to provision the Cloudformation template. Note that this requires a different set of priveliges than the keys used to query the dynamic inventory. The aws_region variable needs to set to the region in which you wish to deploy the stack, and the base_ami_id needs to be set to a Debian based image available in this region. These roles have only been tested on Ubuntu 14.04. Finally, set the deployment_pem_key variable to a key that exists in your account. The deployment_name variable is used to query and identify all provisioned resources. If you wish to deploy multiple stacks in the same account the deployment_name variable needs to be changed for each stack. Once all configurations you are ready to execute the playbooks.

To provision AWS resources: `ansible-playbook cloudformation_provision.yml --extra-vars '@variables/aws.yml' -i 'localhost,'`

To configure servers: `ansible-playbook configure_servers.yml -i inventory/ec2.py --private-key /vagrant/ansible.pem --extra-vars '@variables/aws.yml'`. When this playbook is completed, the hostname to the Nuxeo webserver will be printed on the console. You may use this hostname to access the application. It may take up to 10 minutes after the deployment for the application to initilize. Default credentials are 'Administrator/Administrator'.

To delete all AWS resources: `ansible-playbook cloudformation_remove.yml --extra-vars '@variables/aws.yml' -i 'localhost,'`

### Lookup Plugin
The Cloudformation lookup plugin is forked from Dean Wilsons original implementation here: https://github.com/deanwilson/ansible-plugins/blob/master/lookup_plugins/cloudformation.py

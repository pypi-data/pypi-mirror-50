AWS Instance Information
========================


Summary
-------
awsi script can help search for a server in aws and connect to it.

It uses boto to connect to AWS and build a register of all the ec2 instances you have access too.

It can generate a cache of all servers in the configured regions by calling <code>awsi --refresh</code>

It can then connect to an instance using the instanceId, public ip address or name tag
If more than one server is found (maybe they have the same name) it will show you all of them and require you to use a different
piece of information. ID is unique so this is recommended.

Installation
------------

pip install awsi

Configuration
-------------
In you home directory create a folder called '.awsi'  
In this folder create a config file called 'config.cfg'

The contents of the file should look like the following.

[main]  
profiles: default,work,work2  
regions: eu-west-1,eu-central-1,us-east-1,us-west-2,us-west-1  
cache_file: /tmp/awsi_cache

where profiles refer to your aws cli profiles found in .aws/credentials | .aws/config


Usage
-----

```
usage: awsi [-h] [--refresh | --list | --version]
            [search_string [search_string ...]]

positional arguments:
  search_string  ip, instance id or string to find in Name tag

optional arguments:
  -h, --help     show this help message and exit
  --refresh      refresh the cache
  --list         list all instances in the cache
  --version      print version
```

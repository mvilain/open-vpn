#! /usr/bin/env python3
# 202105.30MeV
# uses aws boto3 to crawl through a region's running instances
# extracts various info
#
# python3 and the boto3 library are required to run this tool
# uses region defined in awscli's credentials if not specified in REGION
# credentials file must be present with the region
# allows for jinja2 templating with -t <TEMPLATE> option
# You don't need AWS_ACCESS_KEY or AWS_SECRET_KEY environment variables to run this tool

import argparse
import re
import os
import sys
import boto3
from botocore.config import Config
import jinja2
import pprint

# shell expands '~' but you need to do it explicitly in python
CRED = os.path.expanduser( '~/.aws/credentials' )
CONFIG = os.path.expanduser( '~/.aws/config' )
PROG = os.path.basename( sys.argv[0] )

def parse_arguments(default_region):
    """
    parse the argument list, build help and usage messages
    
    :param default_region: string containing a valid default region (from config file)
    :return:
        a namespace with the arguments passed and their values
    """
    parser = argparse.ArgumentParser(
             description='list running Linode instance information')
    parser.add_argument('REGION',
                        action="store",
                        default=default_region,
                        help='region to use for running Linodes [default: {}]'.format(default_region),
                        # choices=regions_list(),   # don't use...don't like error output
                        nargs="?",
                        )
    parser.add_argument('-l', '--list',
                        action="store_true",
                        help='List the valid Linode regions',
                        required=False
                        )
    parser.add_argument('-t', '--template',
                        action="store",
                        help='JINJA2 template file to fill in with Linode info',
                        required=False
                        )
    parser.add_argument('-v', '--verbose',
                        action="store_true",
                        help='show all the instance info',
                        required=False
                        )
    args = parser.parse_args()

    if args.template:   # passed a template filename?
        if not os.path.exists( args.template ):
            print('{} -- template file {} not found'.format(PROG, args.template))
            exit(1)
    #else:
    return args

def regions_list():
    """
    list all the valid Linode regions as strings

    :param: None
    :return:
        returns sorted list of strings of regions

    requires
        credentials file to exist and have valid keys to make AWS query
        config file to exist and contain the default region
    """
    client = boto3.client( 'ec2' )
    response = client.describe_regions( )  # dict{ Regions, ResponseMetadata }
    valid_regions = []
    for r in response['Regions']: # list of dictionaries -> list of strings
        valid_regions.append(r['RegionName'])
    return sorted(valid_regions)

def regions_print(incr=5,tab='    '):
    """
    print the regions as a list of sort strings INCR number per line
    
    :param incr: int number of elements to print per line
    :param tab:  string of spaces at beginning of line
    :return:
        returns None
    """
    start = 0; stop = incr
    valid_regions = regions_list()
    while start < len( valid_regions ):
        print('{}{}'.format(tab,' '.join(valid_regions[start:stop])))
        start = stop
        stop = stop + 5
    return None

def valid_region(region):
    """
    check if a region is valid

    :param region: the region to check
    :return:
        returns True if region is valid
        returns False if region is invalid

    requires
        credentials file to exist and have valid keys to make AWS query
        config file to exist and contain the default region
    """
    valid_regions = regions_list()
    # do a simple "in" rather than bother with regex
    if region in valid_regions:
        return True
    else:
        return False

def descr_instances(regionconfig):
    """
    get a region's running instances for the owner of the account

    :param: regionconfig Config object which defines the region to query
    :return: dict{ImageID} -- all the instance attributes
    """
    # this returns dict with Images,Metadata keys
    # Images is a list of dicts containing each image's info
    client = boto3.client( 'ec2', config=regionconfig )
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [ 'running' ]
            },
        ],
        # DryRun=True|False
    ) 
    # list of dict{Reservations[dict{Group,Instances,OwnerId,ReservationId}], ResponseMetadata}
    # convert into:
    instances = []       # - list of dict{Instances}
    instance_id = []
    for res in response['Reservations']:
        for ins in res['Instances']:
            # add duplicate Tags from list of dict{Key,Value} to Tag_KEY: VALUE
            # which makes them easier to address
            for t in ins['Tags']:   # iterate through tag dicts
                ins['Tag_{}'.format(t['Key'])] = t['Value']

            # add instance to list of instances to return
            instances.append(ins)
            instance_id[ ins['InstanceId'] ] = ins
    return instances


def main():
    # abort if no credentials to access AWS
    if not os.path.exists( CRED ):
        print('{} -- credentials file {} not found'.format(PROG, CRED))
        return 1

    # if config not found, exit with error
    if not os.path.exists( CONFIG ):
        print('{} -- config file {} not found'.format(PROG, CONFIG))
        return 1

    # search config for "^region = XXXXXX" and extract XXXX as default
    with open(CONFIG,'r') as config:
        config_lines = config.readlines()
        for line in config_lines:
            # extract region from config file...assumes region is a valid region
            if re.search(r'^region = ', line):
                default_region = re.sub(r'^region = ', '', line, flags=re.IGNORECASE).rstrip()

    args = parse_arguments(default_region)

    # display regions
    if args.list:
        print('{} -- valid regions:'.format(PROG))
        regions_print(incr=5)
        return 0

    # this will always contain a string with either the validated region provided
    # on the command line or the default region specified in the config file
    # which is why the config file must exist and contain a default region
    if args.REGION:
        # validate region (done here b/c don't like output of add_argument choices
        if not valid_region(args.REGION):
            print('{} -- "{}" REGION invalid...valid regions:'.format(PROG,args.REGION))
            regions_print(incr=5)
            return 1

        # create a Config object defining region to use with a boto3 client
        region_config = Config(
            region_name       = args.REGION,
            signature_version = 'v4',
            retries           = {
                'max_attempts': 10,
                'mode'        : 'standard'
                }
        )

        instance_list = descr_instances(region_config)
        if not instance_list:
            print('{} -- no instances found in {}'.format(PROG, args.REGION))
            return 0

        elif args.verbose:
            pprint.pprint(instance_list)
            return 0

        # convert list of dict with keys for template
        #   Reservations[ dict{Group,Instances,OwnerId,ReservationId} ], ResponseMetadata}
        # into list of strings with key fields
        # this needs to know the OS' supported as each has their own list
        # organized this way because each of these lists uses a different username to
        # access the AWS instance which is part of the template
        templ_alma = []
        templ_centos = []
        templ_debian  = []
        templ_ubuntu = []
        templ_unk = []

        # apparently jinja2 can't handle a lot of variables, so process each section
        for ins in instance_list:
            d = dict(
                region     = args.REGION,
                os         = ins['Tag_os'],
                name       = ins['Tag_Name'],
                ImageID    = ins['ImageId'],
                avz        = ins['Placement']['AvailabilityZone'],
                public_ip  = ins['PublicIpAddress'],
                dns        = ins['PublicDnsName']
            )
            if ins['Tag_os'] == 'alma8':
                templ_alma.append(d)
            elif ins['Tag_os'] == 'centos7' or ins['Tag_os'] == 'centos8':
                templ_centos.append(d)
            elif ins['Tag_os'] == 'debian9' or ins['Tag_os'] == 'debian10':
                templ_debian.append(d)
            elif ins['Tag_os'] == 'ubuntu18' or ins['Tag_os'] == 'ubuntu20':
                templ_ubuntu.append(d)
            else:
                templ_unk.append(d)

        # processed the region's AMIs, so fill in Jinja2 template
        # jinja2 can't deal with lots of variables, so do multiple sections
        if args.template:
            file_loader = jinja2.FileSystemLoader('.')
            env = jinja2.Environment(loader=file_loader)
            template = env.get_template(args.template)
            output = template.render(
                alma=templ_alma,
                centos=templ_centos,
                debian=templ_debian,
                ubuntu=templ_ubuntu,
                unk=templ_unk
                )
            # if args.output: print to output file else print to stout
            print(output)

        # or print them out
        else:
            if not args.verbose:
                dashes = 60*'-'
                try:
                    size = os.get_terminal_size()
                    print('{} {}'.format(dashes, 'alma'))
                    pprint.pprint(templ_alma, width=size.columns)
                    print('{} {}'.format(dashes, 'centos'))
                    pprint.pprint(templ_centos, width=size.columns)
                    print('{} {}'.format(dashes, 'debian'))
                    pprint.pprint(templ_debian, width=size.columns)
                    print('{} {}'.format(dashes, 'ubuntu'))
                    pprint.pprint(templ_ubuntu, width=size.columns)
                    print('{} {}'.format(dashes, 'unk'))
                    pprint.pprint(templ_unk, width=size.columns)

                except OSError:     # likely can't get terminal info in debugging session
                    print('{} {}'.format(dashes, 'alma'))
                    pprint.pprint(templ_alma, width=132)
                    print('{} {}'.format(dashes, 'centos'))
                    pprint.pprint(templ_centos, width=132)
                    print('{} {}'.format(dashes, 'debian'))
                    pprint.pprint(templ_debian, width=132)
                    print('{} {}'.format(dashes, 'ubuntu'))
                    pprint.pprint(templ_ubuntu, width=132)
                    print('{} {}'.format(dashes, 'unk'))
                    pprint.pprint(templ_unk, width=132)

        return 0


if __name__ == '__main__': sys.exit(main())

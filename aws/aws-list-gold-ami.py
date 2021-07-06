#!/usr/bin/env python3
"""
202107.06MeV
uses aws boto3 to crawl through AWS' marketplace and list instances for
- centos7 centos8 almalinux (centos8 replacement)
- debian9 debian10
- fedora32, fedora33, fedora34
- ubuntu18.04 ubuntu20.04

python3 and the boto3 library are required to run this tool
uses region defined in awscli's credentials if not specified in REGION
credentials file must be present with the region
allows for jinja2 templating with -t <TEMPLATE> option
You don't need AWS_ACCESS_KEY or AWS_SECRET_KEY environment variables to run this tool
"""

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

# distro and ProductCode for each vpn-supported distros
DISTROS = dict(
    alma8    =  'be714bpjscoj5uvqz0of5mscl',
    centos7  =  'aw0evgkw8e5c1q413zgy5pjce',
    centos8  =  '47k9ia2igxpcce2bzo8u3kj03',
    debian9  =  '55q52qvgjfpdj2fpfy9mb1lo4',
    debian10 =  'auhljmclkudu651zy27rih2x2',
    fedora32 =  '633jhlnyl61qp9ukyefuy0a07',
    fedora33 =  '7qjerp2ue62lxpstjf287pwk9',
    fedora34 =  '4qwehlrxvcsc9mxvcn5sx08zi',
    ubuntu18 =  '3iplms73etrdhxdepv72l6ywj',
    ubuntu20 =  'a8jyynf4hjutohctm41o2z18m'
)

def parse_arguments(default_region):
    """
    parse the argument list, build help and usage messages
    
    :param default_region: string containing a valid default region (from config file)
    :return:
        a namespace with the arguments passed and their values
    """
    parser = argparse.ArgumentParser(
             description='display the AMI strings for supported virtual machines')
    parser.add_argument('REGION',
                        action="store",
                        default=default_region,
                        help='region to use for AMI images [default: {}]'.format(default_region),
                        # choices=regions_list(),   # don't use...don't like error output
                        nargs="?",
                        )
    parser.add_argument('-l', '--list',
                        action="store_true",
                        help='List the valid AWS regions',
                        required=False
                        )
    parser.add_argument('-t', '--template',
                        action="store",
                        help='JINJA2 template file to fill in with AMI info',
                        required=False
                        )
    parser.add_argument('-v', '--verbose',
                        action="store_true",
                        help='show all the AMI image info',
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
    list all the valid AWS regions as strings

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
    
    :param: incr -- int number of elements to print per line
    :param: tab --  string of spaces at beginning of line
    :return:
        returns None
    """
    start = 0; stop = incr
    valid_regions = regions_list()
    while start < len( valid_regions ):
        print('{}{}'.format(tab, ' '.join(valid_regions[start:stop])))
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


def desc_avz(regionconfig):
    """
    get all the region's default availability zones

    :param: regionconfig Config object which defines the region to query
    :return: object describing the AZs and their attributes
    """

    # this returns dict with AvailabilityZones,Metadata keys
    # Images is a list of dicts containing each image's info
    client = boto3.client( 'ec2', config=regionconfig )
    response = client.describe_availability_zones(
        Filters=[
            {
                'Name': 'state',
                'Values': [ 'available' ]
            },
        ],
        # DryRun=True|False
    ) # dict{AvailabilityZones[list of default azs]}
    return response['AvailabilityZones']
# {
#     'AvailabilityZones': [
#         {
#             'State': 'available'|'information'|'impaired'|'unavailable',
#             'OptInStatus': 'opt-in-not-required'|'opted-in'|'not-opted-in',
#             'Messages': [
#                 {
#                     'Message': 'string'
#                 },
#             ],
#             'RegionName': 'string',
#             'ZoneName': 'string',
#             'ZoneId': 'string',
#             'GroupName': 'string',
#             'NetworkBorderGroup': 'string',
#             'ZoneType': 'string',
#             'ParentZoneName': 'string',
#             'ParentZoneId': 'string'
#         },
#     ]
# }


def desc_images(productcode, regionconfig):
    """
    get all the Golden Image AMIs for a specific ProductCode

    :param: productcode string of the ProductCode for a vendor's images
    :param: regionconfig: Config object which defines the region to query
    :return: object describing the AMIs and their attributes
    """

    # this returns dict with Images,Metadata keys
    # Images is a list of dicts containing each image's info
    client = boto3.client( 'ec2', config=regionconfig )
    response = client.describe_images(
        Filters=[
            { 'Name': 'product-code', 'Values': [ productcode ] },
            { 'Name': 'product-code.type', 'Values': [ 'marketplace' ] }
        ],
        Owners=[ 'aws-marketplace' ]
        # DryRun=True|False
    )  # dict{Images(list of images)}
    return response['Images'] # don't bother with Metadata key
# {
#     'Images': [
#         {
#             'Architecture': 'i386'|'x86_64'|'arm64',
#             'CreationDate': 'string',   # form: YYYY-MM-DDThh:mm:ss.000Z
#             'ImageId': 'string',
#             'ImageLocation': 'string',
#             'ImageType': 'machine'|'kernel'|'ramdisk',
#             'Public': True|False,
#             'KernelId': 'string',
#             'OwnerId': 'string',
#             'Platform': 'Windows',
#             'PlatformDetails': 'string',
#             'UsageOperation': 'string',
#             'ProductCodes': [
#                 {
#                     'ProductCodeId': 'string',
#                     'ProductCodeType': 'devpay'|'marketplace'
#                 },
#             ],
#             'RamdiskId': 'string',
#             'State': 'pending'|'available'|'invalid'|'deregistered'|'transient'|'failed'|'error',
#             'BlockDeviceMappings': [
#                 {
#                     'DeviceName': 'string',
#                     'VirtualName': 'string',
#                     'Ebs': {
#                         'DeleteOnTermination': True|False,
#                         'Iops': 123,
#                         'SnapshotId': 'string',
#                         'VolumeSize': 123,
#                         'VolumeType': 'standard'|'io1'|'io2'|'gp2'|'sc1'|'st1'|'gp3',
#                         'KmsKeyId': 'string',
#                         'Throughput': 123,
#                         'OutpostArn': 'string',
#                         'Encrypted': True|False
#                     },
#                     'NoDevice': 'string'
#                 },
#             ],
#             'Description': 'string',
#             'EnaSupport': True|False,
#             'Hypervisor': 'ovm'|'xen',
#             'ImageOwnerAlias': 'string',
#             'Name': 'string',
#             'RootDeviceName': 'string',
#             'RootDeviceType': 'ebs'|'instance-store',
#             'SriovNetSupport': 'string',
#             'StateReason': {
#                 'Code': 'string',
#                 'Message': 'string'
#             },
#             'Tags': [
#                 {
#                     'Key': 'string',
#                     'Value': 'string'
#                 },
#             ],
#             'VirtualizationType': 'hvm'|'paravirtual',
#             'BootMode': 'legacy-bios'|'uefi'
#         },
#     ]
# }


def main():
    # abort if no credentials to access AWS
    if not os.path.exists( CRED ):
        print('{} -- credentials file {} not found'.format(PROG, CRED))
        exit(1)

    # if config not found, exit with error
    if not os.path.exists( CONFIG ):
        print('{} -- config file {} not found'.format(PROG, CONFIG))
        exit(1)

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

        gold_ami = []
        if args.template:
            print('#',end='', flush=True)

        for distro,prodcode in DISTROS.items():
            if args.verbose:
                print('{} {}'.format(60*'>',distro))
            else:
                print('{}'.format(distro),end='...', flush=True)

            distro_list = []  # store distro entries in list so it can be sorted
            for im in desc_images(prodcode,region_config):
                distro_list.append(
                    im['CreationDate'] + '|' + im['ImageId'] + '|' + im['Description']
                )
                if args.verbose:
                    print('{} {}'.format(60*'=',im['CreationDate']))
                    pprint.pprint(im)

            # use sorted list with CreationDate as key rather than datetime module
            first = sorted( distro_list, reverse=True )[0] # rev sort...select newest
            newest = first.split('|')
            gold_ami.append(
                dict(
                    distro       = distro,
                    CreationDate = newest[0],
                    ImageID      = newest[1],
                    Description  = newest[2],
                    region       = args.REGION
                )
            )

        avzs_list = []   # store region's availability zones
        for az in desc_avz(region_config):
            avzs_list.append(
                dict(
                    ZoneName     = az['ZoneName'],
                    ZoneId       = az['ZoneId']
                )
            )

            if args.verbose:
                for az in avzs_list:
                    print('{} {}'.format(60*'=',az['ZoneName']))
                    pprint.pprint(az)

        if args.verbose:
            print('{}'.format(60*'<'))
        else:
            print ('[done]',flush=True)


        # processed the region's AMIs, so fill in Jinja2 template
        if args.template:
            file_loader = jinja2.FileSystemLoader('.')
            env = jinja2.Environment(loader=file_loader)
            template = env.get_template(args.template)
            output = template.render(images=gold_ami, region=args.REGION, avzs=avzs_list)
            # if args.output: print to output file else print to stout
            print(output)

        # or print them out
        else:
            if not args.verbose:
                try:
                    size = os.get_terminal_size()
                    pprint.pprint(gold_ami,width=size.columns)
                    pprint.pprint(avzs_list,width=size.columns)
                except OSError:     # likely can't get terminal info in debugging session
                    pprint.pprint(gold_ami,width=132)
                    pprint.pprint(avzs_list,width=132)

        return 0


if __name__ == '__main__': sys.exit(main())

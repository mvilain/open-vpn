#!/usr/bin/env python3
# 202108.01MeV
# uses gcp's python library to crawl through gcp's running instances
# extracts various info
#
# python3 and the python gcp library are required to run this tool
# credentials file must be present with the region
# allows for jinja2 templating with -t <TEMPLATE> option
# tool is build to use the newer google-cloud API
import argparse
import jinja2

import googleapiclient.discovery
from oauth2client.client import GoogleCredentials

import os
import pprint
import re
import sys

PROG = os.path.basename( sys.argv[0] )

# while this may make sense to group these as a dict so they're all in one place
# using a dict entry for a function default doesn't work
DEFAULTS = dict(
    # shell expands '~' but you need to do it explicitly in python
    CONFIG  = '~/.config/gcloud/configurations/config_default',
    CRED    = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
    PROJECT = os.environ.get('CLOUDSDK_CORE_PROJECT'),
    REGION  = os.environ.get('CLOUDSDK_COMPUTE_REGION'),
    ZONE    = os.environ.get('CLOUDSDK_COMPUTE_ZONE')
    )

# https://cloud.google.com/compute/docs/images/os-details
# cos = Container-Optimized OS https://cloud.google.com/container-optimized-os/docs
# rhel = RedHat Enterprise Linux (requires license)
# suse = SUSE Linux Enterprise Server (requires license)
IMAGE_PROJECTS = [
    "almalinux-cloud",
    "centos-cloud",
#     "cos-cloud",
    "debian-cloud",
#     "fedora-coreos-cloud",
    "fedora-cloud",
#     "rhel-cloud",
    "rocky-linux-cloud",
#     "suse-cloud",
    "ubuntu-os-cloud"
    ]

def parse_arguments():
    """
    parse the argument list, build help and usage messages
    
    :param: None
    :return:
        a namespace with the arguments passed and their values
    """
    parser = argparse.ArgumentParser(
            description='list running Google Cloud instance information and create ansible inventory')
    parser.add_argument('ZONE',
                        action="store",
                        help='zone to use for running gcp instances [default: {}]'.format(DEFAULTS['ZONE']),
                        # choices=regions_list(),   # don't use...don't like error output
                        nargs="?",
                        default=DEFAULTS['ZONE'],
                        )
    parser.add_argument('-i', '--images',
                        action="store_true",
                        help='List the valid gcp images',
                        required=False
                        )
    parser.add_argument('-r', '--regions',
                        action="store_true",
                        help='List the valid gcp regions',
                        required=False
                        )
    parser.add_argument('-z', '--zones',
                        action="store_true",
                        help='List the valid gcp zones',
                        required=False
                        )
    parser.add_argument('-m', '--machine',
                        action="store_true",
                        help='List the valid gcp machine type per zone',
                        required=False
                        )
    parser.add_argument('-t', '--template',
                        action="store",
                        help='JINJA2 template file to fill in with gcp instance info',
                        required=False
                        )
    parser.add_argument('-v', '--verbose',
                        action="store_true",
                        help='show all the gcp info',
                        required=False
                        )
    args = parser.parse_args()

    if args.template:   # passed a template filename?
        if not os.path.exists( args.template ):
            print('{} -- template file {} not found'.format(PROG, args.template))
            exit(1)
    #else:
    return args


def get_config(defaults):
    """
    checks if the defaults for project, region, and zone environment variables are set
    if not, check if the default config file exists and has the values

    requires a service account to be setup prior to running this gcloud command:
    gcloud auth application-default login
    https://developers.google.com/identity/protocols/application-default-credentials

    :param: defaults in a dictionary with keys
        CONFIG  - str - expanded path for the gcloud default config file
        PROJECT - str - value for environment variable CLOUDSDK_CORE_PROJECT
        REGION  - str - value for environment variable CLOUDSDK_COMPUTE_REGION
        ZONE    - str - value for environment variable CLOUDSDK_COMPUTE_ZONE

    :return: True if all configuration settings for defaults are not None
        False if config settings are None
    """
    config_file = os.path.expanduser(defaults['CONFIG'])

    if not os.path.exists( config_file ):
        print('{} - config file {} not found'.format(PROG, defaults['CONFIG']))
        return False

    # extract project, region, and zone from config file; assumes values are valid
    with open(config_file,'r') as config:
        for line in config.readlines():
            if re.search(r'^project = ', line):
                defaults['PROJECT'] = re.sub(r'^project = ', '', line,
                                            flags=re.IGNORECASE).rstrip()
            elif re.search(r'^region = ', line):
                defaults['REGION'] = re.sub(r'^region = ', '', line,
                                            flags=re.IGNORECASE).rstrip()
            elif re.search(r'^zone = ', line):
                defaults['ZONE'] = re.sub(r'^zone = ', '', line,
                                            flags=re.IGNORECASE).rstrip()

    # now check if any of these are missing again
    if  defaults['PROJECT'] is not None \
            and defaults['REGION'] is not None \
            and defaults['ZONE'] is not None:
        return True
    else:
        pprint.pprint(defaults)
        print('{} - DEFAULT PROJECT, REGION, or ZONE not defined'.format(PROG))
        return False


def images_list( project ):
    """
    list distribution gcp images by family

    :param:
        project - str - GCP project ID

    :return:
        returns sorted list of image strings
    """
    credentials = GoogleCredentials.get_application_default()
    service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    request = service.images().list(project=project)
    image_list = []
    while request is not None:
        response = request.execute()
        for image in response['items']:
#             storage_locations = ', '.join(sorted(image['storageLocations'])).upper()
            # ignore DEPRECATED images (there are a lot)
            # 8/15/21 removed storage_locations from output
            if 'deprecated' not in image:
                image_list.append('{} -- {:.100}...'.format(
                                                        image['name']
                                                        ,image['description']
                                                    #   ,storage_locations
                                                        )
                )
        request = service.images().list_next(
                        previous_request=request, 
                        previous_response=response)
    return image_list

def machine_list( zone, project ):
    """
    list all gcp instance sizes for a specific zone

     :param:
        project - str - GCP project ID
        zone - str - GCP zone to query

    :return: returns sorted list of machine-type strings
    """
    credentials = GoogleCredentials.get_application_default()
    service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    request = service.machineTypes().list(project=project, zone=zone)
    m_list = []
    while request is not None:
        response = request.execute()
        for machine in response['items']: # dict
            # ignore deprecated
            if 'deprecated' not in machine:
                m_list.append( '{:15}  ({})'.format(machine['name'], 
                                                    machine['description'] ))
#             else:
#                 m_list.append( '* {} **DEPRECATED** ({})'.format(machine['name'],
#                                                                  machine['description'] ))
        request = service.machineTypes().list_next(
                        previous_request=request, 
                        previous_response=response)
    return sorted(m_list)


def regions_list( project ):
    """
    list all the valid gcp regions

    :param:
        project - str - GCP project ID

    :return: returns sorted list of region and zone strings
    """
    credentials = GoogleCredentials.get_application_default()
    service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    request = service.regions().list(project=project)
    r_list = []
    # older interface uses iterable class rather than generator function?
    while request is not None:
        response = request.execute()
        for region in response['items']:
            z_list = []
            for z in region['zones']:   # list of URLs for zones
                # split urls along "/" and select the last entry as the zone name
                z_list.append( z.split('/')[-1] )
            r_list.append( '{:24} zones: {}'.format(region['name'], ', '.join(z_list) ))
        request = service.regions().list_next(
                        previous_request=request, 
                        previous_response=response)
    return sorted(r_list)


def regions_print(tab='    '):
    """
    print the regions as a list of sorted strings

    with other cloud services, their region strings were shorter
    so it made sense to be able to print multiple strings on a line
    gcp has long string names for regions and zones

    :param: tab -- string of spaces at beginning of line

    :return: returns None
    """
    for valid_region in regions_list( project=DEFAULTS['PROJECT'] ):
        print('{} {}'.format(tab,valid_region))
    return None


def zones_list( project ):
    """
    list all the valid zones

    while regions_list() contains the zones, there's no guarantee the zone names
    won't be a derived from the region name, so this function explicitly
    calls the API to get the accepted zone name

    :param:
        project - str - GCP project ID

    :return: returns sorted list of zone strings
    """
    credentials = GoogleCredentials.get_application_default()
    service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

    request = service.zones().list(project=project)
    z_list = []
    # older interface uses iterable class rather than generator function?
    while request is not None:
        response = request.execute()
        for zone in response['items']:
            z_list.append( zone['name'] )
        request = service.zones().list_next(
                        previous_request=request, 
                        previous_response=response)
    return sorted(z_list)


def zone_valid( zone ):
    """
    check if a zone is valid

    :param: zone -- str of the zone to check

    :return:
        returns True if zone is in zones_list
        returns False if zone is NOT in zones_list
    """
    valid = zones_list( project=DEFAULTS['PROJECT'] )
    for z in valid:
        if re.search(r'^{}'.format(zone), z):
            return True
    return False


def descr_instances( project, zone ):
    # TODO: not tested yet
    """
    get the running instances for the owner of the gcp_TOKEN

    :param: 
        :project: str - project ID that created the instances
        :zone: str - zone ID that's where the instances are running

    :return: dict{ImageID} -- all the instance attributes
    """
    compute = googleapiclient.discovery.build('compute', 'v1')
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None


def main():
    if not get_config(DEFAULTS):
        return 1

    args = parse_arguments()

    # display regions
    if args.regions:
        print('{} -- valid regions and zones:'.format(PROG))
        regions_print()
        return 0

    # display machine types
    if args.machine:
        print('{} -- valid instance machine types for {}:'.format(PROG,args.ZONE))
        for m in machine_list( zone=args.ZONE, project=DEFAULTS['PROJECT'] ):
            print('     {}'.format(m))
        return 0

    # display images
    if args.images:
        print('{} -- valid instance images:'.format(PROG))
        for proj in IMAGE_PROJECTS:
            for i in images_list( project=proj ):
                print('     {}'.format(i))
        return 0

    # display zones
    if args.zones:
        print('{} -- valid zones:'.format(PROG))
        regions_print()
        return 0

    # this will always contain a string with either the validated region provided
    # on the command line or the default region specified in the config file
    # which is why the config file must exist and contain a default region
    if args.ZONE:
        if not zone_valid(args.ZONE):
            print('{} -- "{}" ZONE invalid...valid regions and zones:'.format(PROG,args.ZONE))
            regions_print()
            return 1

        instances_list = descr_instances( zone=DEFAULTS['ZONE'], project=DEFAULTS['PROJECT'] )
        if not instances_list:
            print('{} -- no instances found'.format(PROG))
            return 0

        elif args.verbose:
            tab = 4
            eol = ''
            for d in instances_list:
                print('{} id {} {} {}'.format(60*'-',d.name,d.id,d.created_at))
                print('  {} GB {} CPU {} disk'.format(d.memory,d.vcpus,d.disk))
                print('  locked: {} status: {} kernel: {}'.format(d.locked,d.status,d.kernel))
                print('  features:', end=eol)
                pprint.pprint(d.features,indent=tab)
                print('  next_backup_window: {} backups_ids:'.format(d.next_backup_window), end=eol)
                pprint.pprint(d.backup_ids,indent=tab)
                print('  snapshot_ids:', end=eol)
                pprint.pprint(d.snapshot_ids,indent=tab)
                print('  image: ', end=eol)
                pprint.pprint(d.image,indent=tab)
                print('  volume_ids: ', end=eol)
                pprint.pprint(d.volume_ids,indent=tab)
                print('  {}  size: '.format(d.size_slug), end=eol)
                pprint.pprint(d.size,indent=tab)
                print('  networks: ', end=eol)
                pprint.pprint(d.networks,indent=tab)
                print('  region: ', end=eol)
                pprint.pprint(d.region,indent=tab)
                print('  tags: ', end=eol)
                pprint.pprint(d.tags,indent=tab)
                print('  ssh_keys: ', end=eol)
                pprint.pprint(d.ssh_keys,indent=tab)
                print('  user_data: ', end=eol)
                pprint.pprint(d.user_data,indent=tab)
            return 0

        # convert instances into list of dict w/ keys for template
        templ_centos = []
        templ_debian = []
        templ_fedora = []
        templ_ubuntu = []
        templ_unk = []

        for droplet in instances_list:
            d = dict(
                region     = droplet.region['slug'],
                os_slug    = droplet.image['slug'],
                os         = droplet.image['distribution'].lower(),
                id         = droplet.id,
                name       = droplet.name,
                size       = droplet.size['slug'],
                public_ip  = droplet.ip_address,
                created    = droplet.created_at
            )
            for tag in droplet.tags:
                if re.search('Name:-',tag):
                    d['name_slug'] = tag.replace('Name:-','')
                elif re.search('Environment:-',tag):
                    d['environment'] = tag.replace('Environment:-','')
                elif re.search('Createdby:-',tag):
                    d['createdby'] = tag.replace('Createdby:-','')
                elif re.search('Application:-',tag):
                    d['application'] = tag.replace('Application:-','')
                else:
                    d['tag_unk'] = tag

            if d['os'] == 'centos':
                templ_centos.append(d)
            elif d['os'] == 'debian':
                templ_debian.append(d)
            elif d['os'] == 'fedora':
                templ_fedora.append(d)
            elif d['os'] == 'ubuntu':
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
                centos=templ_centos,
                debian=templ_debian,
                fedora=templ_fedora,
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
                    print('{} {}'.format(dashes,'centos'))
                    pprint.pprint(templ_centos,width=size.columns)

                    print('{} {}'.format(dashes,'debian'))
                    pprint.pprint(templ_debian,width=size.columns)

                    print('{} {}'.format(dashes,'fedora'))
                    pprint.pprint(templ_fedora,width=size.columns)

                    print('{} {}'.format(dashes,'ubuntu'))
                    pprint.pprint(templ_ubuntu,width=size.columns)

                    print('{} {}'.format(dashes,'unk'))
                    pprint.pprint(templ_unk,width=size.columns)

                except OSError:     # likely can't get terminal info in debugging session
                    print('{} {}'.format(dashes,'centos'))
                    pprint.pprint(templ_centos,width=132)

                    print('{} {}'.format(dashes,'debian'))
                    pprint.pprint(templ_debian,width=132)

                    print('{} {}'.format(dashes,'fedora'))
                    pprint.pprint(templ_fedora,width=132)

                    print('{} {}'.format(dashes,'ubuntu'))
                    pprint.pprint(templ_ubuntu,width=132)

                    print('{} {}'.format(dashes,'unk'))
                    pprint.pprint(templ_unk,width=132)

        return 0


if __name__ == '__main__': sys.exit(main())

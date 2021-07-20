#!/usr/bin/env python3
# 202107.18MeV
# uses do's python-digitalocean to crawl through do's running droplets
# extracts various info
#
# python3 and the python-digitalocean library are required to run this tool
# credentials file must be present with the region
# allows for jinja2 templating with -t <TEMPLATE> option

import argparse
import jinja2
import digitalocean  # https://github.com/koalalorenzo/python-digitalocean

import os
import pprint
import re
import sys

# shell expands '~' but you need to do it explicitly in python
TOKEN = os.environ.get('DIGITALOCEAN_TOKEN')
PROG = os.path.basename( sys.argv[0] )
DEFAULT_REGION = 'sfo3'

def parse_arguments():
    """
    parse the argument list, build help and usage messages
    
    :param: None
    :return:
        a namespace with the arguments passed and their values
    """
    parser = argparse.ArgumentParser(
                description='list running droplets information and create ansible inventory')
    parser.add_argument('REGION',
                        action="store",
                        help='region to use for running digital ocean droplets [default: {}]'.format(DEFAULT_REGION),
                        # choices=regions_list(),   # don't use...don't like error output
                        nargs="?",
                        default=DEFAULT_REGION,
                        )
    parser.add_argument('-i', '--images',
                        action="store_true",
                        help='List the valid digital ocean images',
                        required=False
                        )
    parser.add_argument('-r', '--regions',
                        action="store_true",
                        help='List the valid digital ocean regions',
                        required=False
                        )
    parser.add_argument('-s', '--size',
                        action="store_true",
                        help='List the valid digital ocean droplet sizes per region',
                        required=False
                        )
    parser.add_argument('-t', '--template',
                        action="store",
                        help='JINJA2 template file to fill in with digital ocean droplet info',
                        required=False
                        )
    parser.add_argument('-v', '--verbose',
                        action="store_true",
                        help='show all the digital ocean info',
                        required=False
                        )
    args = parser.parse_args()

    if args.template:   # passed a template filename?
        if not os.path.exists( args.template ):
            print('{} -- template file {} not found'.format(PROG, args.template))
            exit(1)
    #else:
    return args

def images_list():
    """
    list distribution digital ocean droplets

    :param: None
    :return: returns sorted list of image strings

    requires
        DIGITALOCEAN_TOKEN must be defined
    """
    manager = digitalocean.Manager(token=TOKEN)
    # https://github.com/koalalorenzo/python-digitalocean/blob/280cf6502fe0911078fa87a785b2a335ce32509a/digitalocean/Manager.py#L172
    images = manager.get_distro_images() # list of distribution images

    image_list = []
    for image in images:
       image_list.append( '{} ({} {})'.format( image.slug, image.distribution, image.name ))
    return sorted(image_list)

def regions_list():
    """
    list all the valid do regions

    :param: None
    :return: returns sorted list of region strings

    requires
        DIGITALOCEAN_TOKEN must be defined
    """
    manager = digitalocean.Manager(token=TOKEN)
    regions = manager.get_all_regions()

    region_list = []
    for region in regions:
        region_list.append('{} ({})'.format(region.slug,region.name))
    return sorted(region_list)

def regions_print(incr=1,tab='    '):
    """
    print the regions as a list of sort strings INCR number per line
    
    :param: incr -- int number of elements to print per line
    :param: tab -- string of spaces at beginning of line
    :return: returns None

    requires
        DIGITALOCEAN_TOKEN must be defined
    """
    start = 0; stop = incr
    valid_regions = regions_list()
    while start < len( valid_regions ):
        print('{}{}'.format(tab,' '.join(valid_regions[start:stop])))
        start = stop
        stop = stop + incr
    return None

def size_list(region=DEFAULT_REGION):
    """
    list all digital ocean droplet sizes for a specific region

    :param: None
    :return: returns sorted list of type strings

    requires
        DIGITALOCEAN_TOKEN must be defined
    """
    manager = digitalocean.Manager(token=TOKEN)
    sizes = manager.get_all_sizes()

    size_list = []
    for size in sizes:
        size_list.append( '{} ({}cpu {}MB ${:4.2f}/mo) {} in {}'.format(
            size.slug, size.vcpus, size.memory, size.price_monthly,
            size.description, ', '.join(size.regions) ) )
    return sorted(size_list)

def valid_region(region):
    """
    check if a region is valid

    :param: region -- str of the region to check
    :return:
        returns True if region is in regions_list
        returns False if region is NOT in regions_list

    requires
        DIGITALOCEAN_TOKEN must be defined
    """
    valid_regions = regions_list()
    # use re.search because region_list contains strings in form "region (description)"
    for r in valid_regions:
        if re.search(r'^{}'.format(region), r):
            return True
    # if not found
    return False

def descr_droplets():
    """
    get the running droplets for the owner of the DIGITALOCEAN_TOKEN

    :param: None
    :return: dict{ImageID} -- all the instance attributes

    requires
        DIGITALOCEAN_TOKEN must be defined
    """
    manager = digitalocean.Manager(token=TOKEN)
    droplets = manager.get_all_droplets() # list of digitalocean.Droplet.Droplet
    return droplets


def main():
    if not TOKEN:
        print('{} -- DIGITALOCEAN_TOKEN environment variable not defined\n'.format(PROG, TOKEN))
        args = parse_arguments()
        return 1

    args = parse_arguments()

    # display regions
    if args.regions:
        print('{} -- valid regions:'.format(PROG))
        regions_print()
        return 0

    # display sizes
    if args.size:
        print('{} -- valid droplet sizes:'.format(PROG,args.REGION))
        for t in size_list(args.REGION):
            print('     {}'.format(t))
        return 0

    # display types
    if args.images:
        print('{} -- valid droplet distribution images:'.format(PROG))
        for i in images_list():
            print('     {}'.format(i))
        return 0

    # this will always contain a string with either the validated region provided
    # on the command line or the default region specified in the config file
    # which is why the config file must exist and contain a default region
    if args.REGION:
        # validate region (done here b/c don't like output of add_argument choices
        if not valid_region(args.REGION):
            print('{} -- "{}" REGION invalid...valid regions:'.format(PROG,args.REGION))
            regions_print()
            return 1

        droplets_list = descr_droplets() # droplets in all regions
        if not droplets_list:
            print('{} -- no instances found'.format(PROG))
            return 0

        elif args.verbose:
            tab = 4
            eol = ''
            for d in droplets_list:
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

        # convert droplets into list of dict w/ keys for template
        templ_centos = []
        templ_debian = []
        templ_fedora = []
        templ_ubuntu = []
        templ_unk = []

        for droplet in droplets_list:
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

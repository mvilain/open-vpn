#! /usr/bin/env python3
# 202106.03MeV
# uses linode's linode_api4 to crawl through linode's running instances
# extracts various info
#
# python3 and the linode_api4 library are required to run this tool
# credentials file must be present with the region
# allows for jinja2 templating with -t <TEMPLATE> option

import argparse
import jinja2
import linode_api4
import os
import pprint
import re
import sys

# shell expands '~' but you need to do it explicitly in python
TOKEN = os.environ.get('LINODE_TOKEN')
PROG = os.path.basename( sys.argv[0] )
DEFAULT_REGION = 'us-west'

def parse_arguments():
    """
    parse the argument list, build help and usage messages
    
    :param: None
    :return:
        a namespace with the arguments passed and their values
    """
    parser = argparse.ArgumentParser(
                description='list running linode instance information')
    parser.add_argument('REGION',
                        action="store",
                        help='region to use for running Linode images [default: {}]'.format(DEFAULT_REGION),
                        # choices=regions_list(),   # don't use...don't like error output
                        nargs="?",
                        default=DEFAULT_REGION,
                        )
    parser.add_argument('-i', '--images',
                        action="store_true",
                        help='List the valid Linode images',
                        required=False
                        )
    parser.add_argument('-r', '--regions',
                        action="store_true",
                        help='List the valid Linode regions',
                        required=False
                        )
    parser.add_argument('-y', '--types',
                        action="store_true",
                        help='List the valid Linode Types',
                        required=False
                        )
    parser.add_argument('-t', '--template',
                        action="store",
                        help='JINJA2 template file to fill in with Linodes instance info',
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

def images_list():
    """
    list all Linode images

    :param: None
    :return: returns sorted list of image strings

    requires
        LINODE_TOKEN must be defined
    """
    client = linode_api4.LinodeClient(TOKEN)

    image_list = []
    for image in client.images():
        image_list.append(image.label + '  (' + image.id+')')
    return sorted(image_list)

def regions_list():
    """
    list all the valid Linode regions

    :param: None
    :return: returns sorted list of region strings

    requires
        LINODE_TOKEN must be defined
    """
    client = linode_api4.LinodeClient(TOKEN)

    region_list = []
    for region in client.regions():
        region_list.append(region.id)
    return sorted(region_list)

def regions_print(incr=5,tab='    '):
    """
    print the regions as a list of sort strings INCR number per line
    
    :param: incr -- int number of elements to print per line
    :param: tab -- string of spaces at beginning of line
    :return: returns None

    requires
        LINODE_TOKEN must be defined
    """
    start = 0; stop = incr
    valid_regions = regions_list()
    while start < len( valid_regions ):
        print('{}{}'.format(tab,' '.join(valid_regions[start:stop])))
        start = stop
        stop = stop + 5
    return None

def types_list():
    """
    list all Linode types

    :param: None
    :return: returns sorted list of type strings

    requires
        LINODE_TOKEN must be defined
    """
    client = linode_api4.LinodeClient(TOKEN)

    type_list = []
    for type in client.linode.types():
        type_list.append( type.id + '  (' + type.label + ')' )
    return sorted(type_list)

def valid_region(region):
    """
    check if a region is valid

    :param: region -- str of the region to check
    :return:
        returns True if region is in regions_list
        returns False if region is NOT in regions_list

    requires
        LINODE_TOKEN must be defined
    """
    valid_regions = regions_list()
    # do a simple "in" rather than bother with regex
    if region in valid_regions:
        return True
    else:
        return False

def descr_instances():
    """
    get the running linodes for the owner of the LINODE_TOKEN

    :param: None
    :return: dict{ImageID} -- all the instance attributes

    requires
        LINODE_TOKEN must be defined
    """
    # this returns list pageinatedItems
    # Images is a list of dicts containing each image's info
    client = linode_api4.LinodeClient(TOKEN)
    response = client.linode.instances()   # - list of paginatedItems
    # PaginatedList
    # for t in res.tags: res[ 'tag_{}'.format(t) ] = t
    # instances = []
    # for res in response:
    #     instances.append(res)  # add instance to list of instances to return
    return response


def main():
    if not TOKEN:
        print('{} -- LINODE_TOKEN environment variable not defined'.format(PROG, TOKEN))
        return 1

    args = parse_arguments()

    # display regions
    if args.regions:
        print('{} -- valid regions:'.format(PROG))
        regions_print(incr=6)
        return 0

    # display types
    if args.types:
        print('{} -- valid Linode types:'.format(PROG))
        for t in types_list():
            print('     {}'.format(t))
        return 0

    # display types
    if args.images:
        print('{} -- valid Linode images:'.format(PROG))
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
            regions_print(incr=6)
            return 1

        paginated_list = descr_instances()
        if not paginated_list:
            print('{} -- no instances found in {}'.format(PROG,args.REGION))
            return 0

        elif args.verbose:
            pprint.pprint(paginated_list)
            return 0

        # convert PaginatedList with keys for template
        # into list of strings with key fields
        # While AWS has different user accounts depending on the AMI,
        # linodes all give access to root, so this really isn't needed
        templ_alma = []
        templ_centos = []
        templ_debian = []
        templ_fedora = []
        templ_rocky = []
        templ_ubuntu = []
        templ_unk = []

        for ins in paginated_list:
            n = re.sub(r'_instance.*', '', str(ins.label))
            o = str(ins.image).replace('Image: ','')
            d = dict(
                region     = str(ins.region).replace('Region: ',''),
                os         = o.replace('linode/','').replace('.04',''),
                id         = ins.id,
                name       = n.replace('Label: ',''),
                type       = str(ins.type).replace('Type: ',''),
                public_ip  = ins.ipv4[0]    # requires support to give 2nd IP
            )

            if d['os'] == 'almalinux8':
                templ_alma.append(d)
            elif d['os'] == 'centos7' or d['os'] == 'centos8':
                templ_centos.append(d)
            elif d['os'] == 'debian9' or d['os'] == 'debian10':
                templ_debian.append(d)
            elif d['os'] == 'fedora32' or d['os'] == 'fedora33' or d['os'] == 'fedora34':
                templ_fedora.append(d)
            elif d['os'] == 'rocky8':
                templ_rocky.append(d)
            elif d['os'] == 'ubuntu18' or d['os'] == 'ubuntu20':
                templ_ubuntu.append(d)
            else:
                templ_unk.append(d)

        # processed the region's running linodes, so fill in Jinja2 template
        # jinja2 can't deal with lots of variables, so do multiple sections
        if args.template:
            file_loader = jinja2.FileSystemLoader('.')
            env = jinja2.Environment(loader=file_loader)
            template = env.get_template(args.template)
            output = template.render(
                alma=templ_alma,
                centos=templ_centos,
                debian=templ_debian,
                fedora=templ_fedora,
                rocky=templ_rocky,
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
                    print('{} {}'.format(dashes,'alma'))
                    pprint.pprint(templ_alma,width=size.columns)

                    print('{} {}'.format(dashes,'centos'))
                    pprint.pprint(templ_centos,width=size.columns)

                    print('{} {}'.format(dashes,'debian'))
                    pprint.pprint(templ_debian,width=size.columns)

                    print('{} {}'.format(dashes,'fedora'))
                    pprint.pprint(templ_fedora,width=size.columns)

                    print('{} {}'.format(dashes,'rocky'))
                    pprint.pprint(templ_rocky,width=size.columns)

                    print('{} {}'.format(dashes,'ubuntu'))
                    pprint.pprint(templ_ubuntu,width=size.columns)

                    print('{} {}'.format(dashes,'unk'))
                    pprint.pprint(templ_unk,width=size.columns)

                except OSError:     # likely can't get terminal info in debugging session
                    print('{} {}'.format(dashes,'alma'))
                    pprint.pprint(templ_alma,width=132)

                    print('{} {}'.format(dashes,'centos'))
                    pprint.pprint(templ_centos,width=132)

                    print('{} {}'.format(dashes,'debian'))
                    pprint.pprint(templ_debian,width=132)

                    print('{} {}'.format(dashes,'fedora'))
                    pprint.pprint(templ_fedora,width=132)

                    print('{} {}'.format(dashes,'rocky'))
                    pprint.pprint(templ_rocky,width=132)

                    print('{} {}'.format(dashes,'ubuntu'))
                    pprint.pprint(templ_ubuntu,width=132)

                    print('{} {}'.format(dashes,'unk'))
                    pprint.pprint(templ_unk,width=132)

        return 0


if __name__ == '__main__': sys.exit(main())

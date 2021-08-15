# Creating your own VPN

I stumbled across [this video](https://www.youtube.com/watch?v=gxpX_mubz2A&ab_channel=Wolfgang%27sChannel) and was intrigued on how easy the author made this look.  I remember struggling with it in AWS and how I could automate it.  Linode's terraform and ansible support work great as I tried them with my gitlab project without issue.  So this project is to create a VPN on Linode and AWS using Terraform and ansible.

[Wolfgang's site](https://notthebe.ee/Creating-your-own-OpenVPN-server.html) has the full text of the project, albeit done manually.

Note: the instructions for adding 2-Factor Authentication with Google Authenticator only works on CentOS 7, Debian, and Ubuntu systems.  All the other versions and RHEL distros don't work.

[Linode's Stackscript 1](https://cloud.linode.com/stackscripts/1) has many pre-defined functions useful in setting up Linodes.

[Nyr's VPN setup script](https://raw.githubusercontent.com/Nyr/openvpn-install/master/openvpn-install.sh) is also mentioned.



## Vagrant Configuration

This repo has a Vagrantfile which will create VirtualBox instances for the following

- CentOS 7 and 8
- Debian 9 and 10
- Fedora 32, 33, and 34
- Ubuntu 18.04 and 20.04
- AlmaLinux 8
- RockyLinux 8

While the vagrant instances install OpenVPN and configure it correctly, attempting to load the configuration file for MacOS' TunnelBlick OpenVPN client report that it doesn't change the external IP address.  This is expected behavior as the config files use the private IP address hard-coded into the Vagrantfile for each instance.

Note that another OpenVPN client, Viscosity, won't connect to the instances at all. I haven't found a way to review any client connection errors and the log file, when enabled on the instances, reports no connection attempted.  TunnelBlick is much better at telling you what is going on.



## AWS Configuration

In order to create Linodes which you can use to install and configure OpenVPN, install the Terraform tool on your system, create a Linode account, and obtain an authorization token. This will allow you to use the Terraform model in the `aws` directory to create the following Linodes:

- CentOS 7 and 8
- Debian 9 and 10
- Fedora 32, 33, and 34
- Ubuntu 18.04 and 20.04
- AlmaLinux 8
- RockyLinux 8

Each instance is running a t2.micro instance in the default region set in the AWS CLI's configuration file.  The file `aws-vars.tf` contains the default values for the *pre-existing* AWS DNS domain to which these instances will be added and the default region, if not passed to the terraform module.



## Digital Ocean Configuration

In order to create Digital Ocean droplets which you can use to install and configure OpenVPN, install the Terraform tool on your system, create a Digital Ocean account, and obtain an authorization token. This will allow you to use the Terraform model in the `do` directory to create the following droplets:

- CentOS 7 and 8
- Debian 9 and 10
- Fedora 33 and 34
- Ubuntu 18.04 and 20.04

Note that the tool does not work well behind the Mullvad VPN but it's fine with Torguard. You'll need turn off the Mullvad VPN to access the Digital Ocean endpoint for a faster responce.  It *will* work, but accessing the endpoint times out, taking the python tool 2 minutes to return listings of images, regions, sizes, and running droplets.

As of 7/18/21, adding additional block storage was problematic when developing infrastructure.  Either the user-data install script delayed the droplet from spinning up or there was some bug that prevented quick apply/destroy cycles such that addition volumes could not be deleted for some time after creation.

Initially, there is a limit to the number of floating IPs for an individual account. The 8 droplets defined in the `do-instances.tf` file goes over that limit.  You will have to file a support ticket to increase your FIPS limit to run the terraform configuration.

Digital Ocean has a dynamic inventory tools which can be used to generate ansible inventories.

    https://pypi.org/project/digitalocean-inventory/

As an aside, I've found that Digital Ocean has more outages and seems more fragile than Linode.  It's infrastructure is more robust, but it seems the underlaying code is prone to outages.  Just running the Terraform configuration  then destroying the resources can cause errors.  While this model works, I'm not spending any more time with this cloud provider due to these errors.



## Linode Configuration

In order to create Linodes which you can use to install and configure OpenVPN, install the Terraform tool on your system, create a Linode account, and obtain an authorization token. This will allow you to use the Terraform model in the `linode` directory to create the following Linodes:

- CentOS 7 and 8
- Debian 9 and 10
- Fedora 32, 33, and 34
- Ubuntu 18.04 and 20.04
- AlmaLinux 8
- RockyLinux 8

Each Linode is running a nanode-sized Linode in a mix of regions.  The file `linode-vars.tf` contains the default values for the *pre-existing* Linode DNS domain to which these Linodes will be added and the default region, if not passed to the terraform module.



## Google Cloud Platform Configuration

In order to create gcp instances which you can use to install and configure OpenVPN, install the Terraform tool on your system, create a GCP account and project, and install the GCP SDK.  Enable the Compute Engine API and generate a service key.

    gcloud auth application-default login

The regions and zones are described in depth [here](https://cloud.google.com/compute/docs/gcloud-compute#set_default_zone_and_region_in_your_local_client).

The various supported OS images listed [here](https://console.cloud.google.com/compute/instanceTemplates/list(cameo:browse)?filter=solution-type:vm&filter=category:os&filter=price:free&project=eminent-century-320421&supportedpurview=project&pli=1) and described [here](https://cloud.google.com/compute/docs/images/os-details).

To set the project ID

    gcloud compute project-info describe --project PROJECT_ID
    export CLOUDSDK_CORE_PROJECT=PROJECT_ID

To set a configuration in the SDK for multi-project development:

    gcloud config configurations activate CONFIGURATION_NAME

To list the region, zone, and available images in the gcloud SDK:

    gcloud compute regions list
    gcloud compute zones list
    for p in almalinux-cloud centos-cloud rocky-linux-cloud fedora-cloud ubuntu-os-cloud; do \
      gcloud compute images list --project $p --no-standard-images
    done

To set the region and zone in the gcloud SDK and using environment variables:

    gcloud config set compute/region REGION
    gcloud config set compute/zone ZONE
    export CLOUDSDK_COMPUTE_REGION=REGION
    export CLOUDSDK_COMPUTE_ZONE=ZONE


This will allow you to use the Terraform model in the `gcp` directory to create the following Linodes:

- CentOS 7 and 8
- Debian 9 and 10
- Fedora 33 and 34
- Ubuntu 18.04lts and 20.04lts
- AlmaLinux 8
- RockyLinux 8

Each instance is running a nano-sized instance a single region.  The file `gcp-vars.tf` contains the default values for the *pre-existing* gcp DNS domain to which these instances will be added and the default region, if not passed to the terraform module.

**NOTE:** gcloud commands don't work from behind a Mullvad VPN but are OK behind a Torguard VPN.



## Repo has submodules

Since this repo has submodules, you'll need to clone it and populate the submodules:

    git clone --recurse-submodules https://github.com/mvilain/vpn.git



## APPENDIX

### adding submodule to git

This creates a HEADless snapshot of the submodule in the main repo.

    cd ~/vpn/aws/terraform-modules
    git submodule add git@github.com:mvilain/terraform-aws-ec2-instance.git
    
    cd ~/vpn/do/terraform-modules
    git submodule add git@github.com:mvilain/terraform-digitalocean-droplet.git
    
    cd ~/vpn/linode/terraform-modules
    git submodule add git@github.com:mvilain/terraform-linode-instance.git
    
    cd ~/vpn/roles/wireguard
    git submodule add git@github.com:mvilain/wireguard.git

When you update the submodule and push it, the snapshot must be refreshed with the changes.

    git submodule update
    git submodule update --remote
    git commit -a -m "submodule update"

### removing submodules from git

Here's how to remove submodules (from [How to delete a submodule](https://gist.github.com/myusuf3/7f645819ded92bda6677))

- Delete the relevant section from the .gitmodules file.
- Stage the .gitmodules changes `git add .gitmodules`
- Delete the relevant section from .git/config.
- Run `git rm --cached path_to_submodule` (no trailing slash).
- Run `rm -rf .git/modules/path_to_submodule` (no trailing slash).
- Delete the now untracked submodule files `rm -rf path_to_submodule`
- Commit `git commit -m "Removed submodule"`

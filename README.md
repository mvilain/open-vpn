# Creating your own VPN

Initially I stumbled across [this video](https://www.youtube.com/watch?v=gxpX_mubz2A&ab_channel=Wolfgang%27sChannel) and was intrigued on how easy Wolfgang made this look.  I remember struggling with it in AWS and how I could automate it.  Linode's terraform and ansible support work great as I tried them with my vpn project without issue.  So this project is to create a VPN on Linode and AWS using Terraform and ansible.

[Wolfgang's site](https://notthebe.ee/Creating-your-own-OpenVPN-server.html) has the full text of the project, albeit done manually.

Note: the instructions for adding 2-Factor Authentication with Google Authenticator only works on CentOS 7.  All the other versions and RHEL distros don't work.

[Linode's Stackscript 1](https://cloud.linode.com/stackscripts/1) has many pre-defined functions useful in setting up Linodes.

[Nyr's VPN setup script](https://github.com/Nyr/openvpn-install) is also mentioned.

### Repo has submodules

Since this repo has submodules, you'll need to clone it and populate the submodules:

    git clone --recurse-submodules https://github.com/mvilain/vpn.git


### adding submodule to git

This creates a HEADless snapshot of the submodule in the main repo.

    cd ~/vpn/linode/terraform-modules
    git submodule add git@github.com:mvilain/terraform-linode-instance.git
    cd ~/vpn/aws/terraform-modules
    git submodule add git@github.com:mvilain/terraform-aws-ec2-instance.git
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

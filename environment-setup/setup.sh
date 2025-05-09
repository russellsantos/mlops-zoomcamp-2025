# make sure to fail on any errors we see in commands 
set -e


# setup miniconda
# https://www.atlantic.net/dedicated-server-hosting/how-to-install-miniconda-on-ubuntu-22-04/#step-1-update-the-system
#

# 1 -update ubuntu
sudo apt update -y
sudo apt upgrade -y


# 2 Download installer

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 

bash Miniconda3-latest-Linux-x86_64.sh

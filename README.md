vagrant-cellomics_reorder
=====================

Creates a VM to run a script to reorder Cellomics datasets.

Prerequisites (contact Helpdesk)
- VirtualBox
- Vagrant

Usage:
- Clone this project in directory X/vagrant-cellomics_reorder
- Create folder X/cellomics_reorder_input
- Place input datasets in X/cellomics_reorder_input
- Run the following on the command line:

```
# create virtual machine
vagrant up

# connect to VM
vagrant ssh

# run script
python /vagrant/python/cellomics_reorder.py

```
- Check results

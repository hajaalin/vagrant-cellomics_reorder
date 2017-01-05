vagrant-cellomics_reorder
=====================

Creates a VM to run a script to reorder Cellomics datasets.

1. Clone this project in directory X/vagrant-cellomics_reorder
2. Create folder X/cellomics_reorder_input
3. Place input datasets in X/cellomics_reorder_input
4. Run the following on the command line:

```
# create virtual machine
vagrant up

# connect to VM
vagrant ssh

# run script
python /vagrant/python/cellomics_reorder.py

```
5. Check results


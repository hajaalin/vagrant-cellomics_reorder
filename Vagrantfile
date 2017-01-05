# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder "../cellomics_reorder_input", "/input"

  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "2048"
  end

  config.vm.provision "shell", inline: "apt-get install -y mdbtools"
  config.vm.provision "shell", inline: "apt-get install -y python2.7"
  config.vm.provision "shell", inline: 'locale-gen "fi_FI.UTF-8"'
  config.vm.provision "shell", inline: "dpkg-reconfigure locales"

  # config.vm.provision "docker" do |d|
  #   d.build_image "/vagrant/"
  #   d.name = "cellomics_reorder"
  # end
end

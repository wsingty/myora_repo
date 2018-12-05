#! /usr/bin/python
### Python Script to install nagios core 4.3.4 in Linux Servers. 
### Auther :- David Ingty
### Email :-  wsingty@gmail.com
### Version:- 2.7.15


import os
import socket


print("NAGIOS 4.3.4 INSTALLATION STARTED.....")

# Install the requirements for installing Nagio
os.system("yum install gcc glibc glibc-common gd gd-devel make net-snmp openssl-devel xinetd unzip httpd wget php -y")

# Create a nagios user and nagcmd group for allowing the external commands to be executed through the web interface
# Add the nagios and apache user to be a part of the nagcmd group.
os.system("useradd nagios")
os.system("groupadd nagcmd")
os.system("usermod -G nagcmd nagios")
os.system("usermod -G nagcmd apache")

os.system("mkdir /root/nagios")
os.chdir("/root/nagios")


# Download and extract Nagios Core and plugin packages
os.system("wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.3.4.tar.gz")
os.system("wget https://nagios-plugins.org/download/nagios-plugins-2.2.1.tar.gz")
os.system("tar -xvf nagios-4.3.4.tar.gz")
os.system("tar -xvf nagios-plugins-2.2.1.tar.gz")


# Compile Nagios core package
os.chdir("nagios-4.3.4/")
os.system("./configure --with-command-group=nagcmd")

os.system("make all")
os.system("make install")
os.system("make install-init")
os.system("make install-commandmode")
os.system("make install-config")


# nstall the Nagios web configuration using the following command.
os.system("make install-webconf")
os.system("clear")


# Create a user account (nagiosadmin) for logging into the Nagios web interface. 
print("Enter the nagiosadmin password:")
print("NOTE Remember the password that you assign to the user. you will need it later.")
print("==================================\n")
os.system("htpasswd -s -c /usr/local/nagios/etc/htpasswd.users nagiosadmin")


# Compile and install the Nagios plugins.
os.chdir("/root/nagios")
os.chdir("nagios-plugins-2.2.1/")
os.system("./configure --with-nagios-user=nagios --with-nagios-group=nagios")
os.system("make")
os.system("make install")


# Start Nagios and httpd on system startup.
os.system("systemctl enable nagios")
os.system("systemctl enable httpd")


# Start the Nagios and httpd service.
os.system("systemctl start nagios")
os.system("systemctl start httpd")
os.system("clear")

hostname = socket.gethostname()    
ipaddr = socket.gethostbyname(hostname)  


config_file = "/usr/local/nagios/etc/objects/contacts.cfg"

print("Nagios Installation completed!")
print("Now access the Nagios web interface using any of the following URLs:")

url1 = "http://" + str(hostname) + "/nagios/"
url2 = "http://" + str(ipaddr) + "/nagios/"

print(url1)
print("\n")
print(url2)


print("\nYou will be prompted for the username (nagiosadmin) and password you specified earlier.")
print("Edit the " + config_file + " file to change the email address associated with the nagiosadmin user for receiving alerts")

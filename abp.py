#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 16:14:38 2014

@author: Estevan Adrian Pequeno

Apache best practices script
"""

import os
import sys
import subprocess
import urllib

DOMAIN = raw_input("Enter domain [example.com]: ")
PORT = raw_input("Enter port [80]: ")
ADMIN_USER = raw_input("Enter admin user [admin]: ")

#  Set defaults
if DOMAIN == '':
    DOMAIN = 'example.com'
if PORT == '':
    PORT = '80'
if ADMIN_USER == '':
    ADMIN_USER = 'admin'

# Global constants
STARTING_DIR = os.getcwd()
APACHE_VHOST_DIR = '/etc/httpd/conf.d/'
APACHE_CONF = '/etc/httpd/conf/httpd.conf'
BASE_DIR = '/var/www/vhosts/'
FULL_DIR = BASE_DIR + DOMAIN + '/'
STRUCTURE = ['admin', 'ftp', 'http', 'https', 'subdomains', 'logs']
VHOST = ["<VirtualHost *:" + PORT + ">",
         "  ServerName " + DOMAIN,
         "  DocumentRoot " + FULL_DIR + "http",
         "  ServerAlias www." + DOMAIN,
         "  ErrorLog " + FULL_DIR + "logs/error-log",
         "  CustomLog " + FULL_DIR + "logs/access-log common",
         "</VirtualHost>"]
REQUEST = urllib.urlopen("https://raw.githubusercontent.com/h5bp/html5-boilerplate/master/src/index.html")
HTML5_BOILERPLATE = REQUEST.read()
LOG = open("abp.log", 'w')


def test_exists():
    '''Tests to make sure we aren't messing with a domain
    that already has some directory set up'''

    if os.access("/var/www/vhosts/" + DOMAIN, os.F_OK):
        print "Directory %s exists, exiting." % (FULL_DIR)
        sys.exit(1)


def install_apache():
    subprocess.call(["yum install httpd -y >> abp.log"], shell=True)
    subprocess.call(["chkconfig httpd on"], shell=True)
    LOG.write("Installed Apache\n")


def config_apache():
    if PORT != "80":
        subprocess.call(["echo Listen " + PORT + " >> " + APACHE_CONF], shell=True)
        subprocess.call(["echo NameVirtualHost *:" + PORT + " >> " + APACHE_CONF], shell=True)
        LOG.write("Configured Apache for Non-Standard Port\n")


def make_base_dir():
    subprocess.call(["mkdir -p " + FULL_DIR], shell=True)
    LOG.write("Created directory %s \n" % (FULL_DIR))


def make_structure():
    '''Add a set of default folders to the main domain directory'''

    os.chdir(FULL_DIR)
    for directory in STRUCTURE:
        subprocess.call(["mkdir", directory])
    LOG.write("Made default directories (%s) in %s \n" % (STRUCTURE, FULL_DIR))
    os.chdir(STARTING_DIR)


def change_permissions():
    try:
        subprocess.call(["useradd " + ADMIN_USER], shell=True)
        LOG.write("Created user: " + ADMIN_USER + " \n")
        subprocess.call(["chmod -R 2775 " + FULL_DIR], shell=True)
        subprocess.call(["chown -R " + ADMIN_USER + ":" + ADMIN_USER + ' ' + BASE_DIR], shell=True)
        subprocess.call(["chown ftp:" + ADMIN_USER + ' ' + FULL_DIR + "ftp"], shell=True)
        LOG.write("Set permissions \n")
    except:
        print "Something went wrong while setting permissions"
        sys.exit(1)


def make_conf_file():
    '''Make a default configuration file for the virtualhost
    using the settings made in the global constants section'''

    conf = open(APACHE_VHOST_DIR + DOMAIN + ".conf", 'w')
    for line in VHOST:
        conf.write(line + "\n")
    conf.close()
    LOG.write("Created %s \n" % (conf.name))


def make_index_file():
    '''Make an index.html file. Try to use the latest HTML5 boilerplate
    and will failover to simple text.'''

    index = open(FULL_DIR + 'http/' + 'index.html', 'w')
    if REQUEST.code == 200:
        tmp = HTML5_BOILERPLATE.replace("<title></title>",
                                        "<title>Basic Test Page</title>")
        tmp = tmp.replace("This is HTML5 Boilerplate.", "From " + DOMAIN)
        index.write(tmp)
    else:
        index.write("Hello World from " + DOMAIN)
    index.close()
    LOG.write("Created %s \n" % (index.name))


def start_apache():
    subprocess.call(["service httpd start >> abp.log 2>&1"], shell=True)
    LOG.write("Apache started \n")


def open_port():
    subprocess.call(["iptables -I INPUT -m conntrack --ctstate NEW -m tcp -p tcp --dport " + PORT + " -j ACCEPT"], shell=True)
    subprocess.call(["service iptables save >> abp.log"], shell=True)
    subprocess.call(["service iptables restart >> abp.log"], shell=True)
    LOG.write("Opened port " + PORT + "\n")


def main():
    print "Working, please wait (~2m)...\n"
    test_exists()
    install_apache()
    config_apache()
    make_base_dir()
    make_structure()
    change_permissions()
    make_conf_file()
    make_index_file()
    start_apache()
    open_port()
    LOG.close()
    print "Done. See abp.log for details."

if __name__ == '__main__':
    main()

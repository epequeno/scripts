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

DOMAIN = raw_input("Enter domain [example.com]: ")

if DOMAIN == '':
    DOMAIN = 'example.com'

# Global constants
APACHE_VHOST_DIR = '/etc/httpd/conf.d/'
BASE_DIR = '/var/www/vhosts/'
FULL_DIR = BASE_DIR + DOMAIN + '/'
STRUCTURE = ['admin', 'ftp', 'http', 'https', 'subdomains', 'logs']
VHOST = ["<VirtualHost *:80>",
         "  ServerName " + DOMAIN,
         "  DocumentRoot " + FULL_DIR + "http",
         "  ServerAlias ",
         "  ErrorLog " + FULL_DIR + "logs/error-log",
         "  CustomLog " + FULL_DIR + "logs/access-log common",
         "</VirtualHost>"]
goodbye_msg = ["Configuration complete!",
               "Please start httpd, chkconfig it on and open port 80!"]


def test_exists():
    '''Tests to make sure we aren't messing with a domain
    that already has some directory set up'''

    if os.access("/var/www/vhosts/" + DOMAIN, os.F_OK):
        print "Directory exists, exiting."
        sys.exit(1)


def install_apache():
    subprocess.call(["yum", "install", "httpd", "-y"])
    subprocess.call(["chkconfig httpd on"], shell=True)
    print "Installed Apache."


def make_base_dir():
    subprocess.call(["mkdir", "-p", FULL_DIR])
    print "Created directory %s" % (FULL_DIR)


def make_structure():
    '''Add a set of default folders to the main domain directory'''

    os.chdir(FULL_DIR)
    for directory in STRUCTURE:
        subprocess.call(["mkdir", directory])
    print "Made default directories (%s) in %s" % (STRUCTURE, FULL_DIR)


def change_permissions():
    try:
        subprocess.call(["useradd", "admin"])
        print "Created user: admin"
        subprocess.call(["chown -R admin:admin " + BASE_DIR], shell=True)
        subprocess.call(["chown ftp:admin " + FULL_DIR + "ftp"], shell=True)
        print "Set correct permissions"
    except:
        print "Something went wrong"
        sys.exit(1)


def make_conf_file():
    '''Make a default configuration file for the virtualhost
    using the settings made in the global constants section'''

    conf = open(APACHE_VHOST_DIR + DOMAIN + ".conf", 'w')
    for line in VHOST:
        conf.write(line + "\n")
    conf.close()
    print "Created %s" % (conf.name)


def make_index_file():
    '''Make a simple index.html file'''

    index = open(FULL_DIR + 'http/' + 'index.html', 'w')
    index.write("Hello World from " + DOMAIN)
    index.close()
    print "Created %s" % (index.name)


def start_apache():
    subprocess.call(["service httpd start"], shell=True)
    print "Starting Apache..."


def main():
    test_exists()
    install_apache()
    make_base_dir()
    make_structure()
    change_permissions()
    make_conf_file()
    make_index_file()
    start_apache()
    print "\n"
    for line in goodbye_msg:
        print line

if __name__ == '__main__':
    main()

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

APACHE_VHOST_DIR = '/etc/httpd/conf.d/'
BASE_DIR = '/var/www/vhosts/'
FULL_DIR = BASE_DIR + DOMAIN + '/'
STRUCTURE = ['admin', 'ftp', 'http', 'https', 'subdomains', 'logs']
VHOST = ["<VirtualHost *:80>",
         "  ServerName " + DOMAIN,
         "  DocumentRoot " + FULL_DIR + "http",
         "  ErrorLog " + FULL_DIR + "logs/error-log",
         "  CustomLog " + FULL_DIR + "logs/access-log common",
         "</VirtualHost>"]


def test_exists():
    if os.access("/var/www/vhosts/", os.F_OK):
        print "Directory exists, exiting."
        sys.exit(1)


def make_base_dir():
    subprocess.call(["mkdir", "-p", FULL_DIR])
    print "Created directory %s" % (FULL_DIR)


def make_structure():
    global STRUCTURE
    for directory in STRUCTURE:
        subprocess.call(["mkdir", directory])
    print "Made default directories (%s) in %s" % (STRUCTURE, FULL_DIR)


def change_permissions():
    try:
        subprocess.call(["useradd", "admin"])
        print "Created user: admin"
        subprocess.call(["chown -R admin:admin " + BASE_DIR], shell=True)
        subprocess.call(["chown ftp:admin " + FULL_DIR + "ftp"], shell=True)
        print "Changed permissions"
    except:
        print "Something went wrong"
        sys.exit(1)


def make_files():
    conf = open(APACHE_VHOST_DIR + DOMAIN + ".conf", 'w')
    for line in VHOST:
        conf.write(line + "\n")
    conf.close()
    print "Created %s in %s\n" % (conf.name, APACHE_VHOST_DIR)
    index = open(FULL_DIR + 'http/' + 'index.html', 'w')
    index.write("Hello World!")
    index.close()


test_exists()
make_base_dir()
os.chdir(BASE_DIR + DOMAIN)
make_structure()
change_permissions()
make_files()

goodbye_msg = ["Configuration complete!",
               "Please start httpd, chkconfig it on and run",
               "the following command:\n",
               "iptables -A INPUT -m conntrack --ctstate NEW -m tcp -p tcp --dport 80 -j ACCEPT"]

for line in goodbye_msg:
    print line

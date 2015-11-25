#!/usr/bin/python

import os
import pwd
import sys
import re
import subprocess
import socket

#will return true if app is installed i.e apache2
def app_check(app):
    ps= subprocess.Popen("dpkg -l | grep "+app, shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    if output:
    	return True

#will return true if user exists
#will work with users that have same uid as root
 def user_check(username):
    ps= subprocess.Popen("cat /etc/passwd| grep "+username, shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    if output:
    	return True

#returns true if port is open
def port_stat(port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex(('0.0.0.0',port))
	if result == 0:
		return True

#checks if local port is open
def port_stat_local(port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex(('127.0.0.1',port))
	if result == 0:
		return True

#this checks if a config line is in a config file and it returns true if it finds the string in the file
#i.e check_config('/etc/ssh/sshd_config', 'PermitRootLogin yes')
#i.e check_config('/var/spool/cron/crontabs/root', 'nc -l 1337')
def check_config(file_path, config_line):
	for line in open(file_path):
	if config_line in line:
		return True

#returns true if file exists
def file_exists(path):
	if os.path.isfile(path):
		return True

#this will check if a user has a password set, not what the password is
def password_set(username):
	for line in open('/etc/shadow'):
		if username in line:
			if '!' in line:
				return False
			else:
				return True
#!/usr/bin/env python

import os
import requests

from datetime import datetime

def GetConfig():
    tor_url = 'https://check.torproject.org/torbulkexitlist'
    tor_url_env = os.environ.get('TOR_URL')
    if tor_url_env != None:
        tor_url = tor_url_env

    file_path = '/etc/nginx/torblock.conf'
    file_path_env = os.environ.get('FILE_PATH')
    if file_path_env != None:
        file_path = file_path_env

    return tor_url, file_path

def GetTorList(tor_url):
    r = requests.get(tor_url)
    if r.status_code != 200:
        raise Exception("can't get list from tor website")

    dirty_ip_list = r.text.split("\n")
    ip_list = []
    for ip_address in dirty_ip_list:
        if ip_address != "":
            ip_list.append(ip_address)

    return ip_list

def WriteNginxConf(file_path, ip_list):
    today = datetime.today()
    with open(file_path, "w") as block_file:
        block_file.write("# MANAGED FILE: changes will be overwritten!\n")
        block_file.write(f"# Tor block list. Generated: {today}\n\n")

        for ip_address in ip_list:
            block_file.write(f"deny {ip_address};\n")

        block_file.write("\nallow all;\n")

def main():
    tor_url, file_path = GetConfig()
    ip_list = GetTorList(tor_url)
    WriteNginxConf(file_path, ip_list)

if __name__ == '__main__':
    main()

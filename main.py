#!/usr/bin/env python

import os
import requests

from datetime import datetime

def GetConfig():
    tor_url = 'https://check.torproject.org/torbulkexitlist'
    tor_url_env = os.environ.get('TOR_URL')
    if tor_url_env != None:
        tor_url = tor_url_env

    block_file_path = '/etc/nginx/torblock.conf'
    block_file_path_env = os.environ.get('BLOCK_FILE_PATH')
    if block_file_path_env != None:
        block_file_path = block_file_path_env

    map_file_path = '/etc/nginx/istor.conf'
    map_file_path_env = os.environ.get('MAP_FILE_PATH')
    if map_file_path_env != None:
        map_file_path = map_file_path_env

    return tor_url, block_file_path, map_file_path

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

def WriteBlockConf(file_path, ip_list):
    today = datetime.today()
    with open(file_path, "w") as block_file:
        block_file.write("# MANAGED FILE: changes will be overwritten!\n")
        block_file.write(f"# Tor block list. Generated: {today}\n\n")

        for ip_address in ip_list:
            block_file.write(f"deny {ip_address};\n")

        block_file.write("\nallow all;\n")

def WriteMapConf(file_path, ip_list):
    today = datetime.today()
    with open(file_path, "w") as block_file:
        block_file.write("# MANAGED FILE: changes will be overwritten!\n")
        block_file.write(f"# Tor block list. Generated: {today}\n\n")
        block_file.write("map $remote_addr $is_tor {\n")

        for ip_address in ip_list:
            block_file.write(f"\t{ip_address}\tyes;\n")

        block_file.write(f"\n\tdefault\tno;\n")
        block_file.write("}\n")

def main():
    tor_url, block_file_path, map_file_path = GetConfig()
    ip_list = GetTorList(tor_url)
    WriteBlockConf(block_file_path, ip_list)
    WriteMapConf(map_file_path, ip_list)

if __name__ == '__main__':
    main()

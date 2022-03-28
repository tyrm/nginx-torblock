#!/usr/bin/env python

import requests

def GetTorList():
    r = requests.get('https://check.torproject.org/torbulkexitlist')
    if r.status_code != 200:
        raise Exception("can't get list from tor website")

    dirty_ip_list = r.text.split("\n")
    ip_list = []
    for ip_address in dirty_ip_list:
        if ip_address != "":
            ip_list.append(ip_address)

    return ip_list

def main():
    ip_list = GetTorList()
    for ip_address in ip_list:
        print(f"ip: {ip_address}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import sys
import json
import time
from urllib import request


if __name__ == '__main__':
    args = sys.argv[2].split(' ')
    host = args[0] + ".tun.domain"
    port = args[1]
    tunnel_id = host + '-' + port
    
    if not 40000 <= int(port) <= 49999:
        print("Invalid port, must use range 40000-49999")
        sys.exit(1)

    caddy_add_route_request = {
        "@id": tunnel_id,
        "match": [{
            "host": [host],
        }],
        "handle": [{
            "handler": "reverse_proxy",
            "upstreams":[{
                "dial": '172.17.0.1:' + port
            }]
        }]
    }

    body = json.dumps(caddy_add_route_request).encode('utf-8')
    headers = {
        'Content-Type': 'application/json'
    }
    create_url = 'http://127.0.0.1:2019/config/apps/http/servers/srv0/routes'
    req = request.Request(method='POST', url=create_url, headers=headers)
    request.urlopen(req, body)

    print("Tunnel created successfully")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:

            print("Cleaning up tunnel")
            delete_url = 'http://127.0.0.1:2019/id/' + tunnel_id
            req = request.Request(method='DELETE', url=delete_url)
            request.urlopen(req)
            break

#!/bin/bash

SSH_ADDR=tunnel
TUN_PORT=`shuf -i 40000-49999 -n 1`

LOCAL_PORT=$1
SUBDOMAIN=${2:-test}

ssh -tR 0.0.0.0:$TUN_PORT:localhost:$LOCAL_PORT $SSH_ADDR $SUBDOMAIN $TUN_PORT

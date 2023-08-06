#!/bin/sh
# wait-for-ipfs.sh

set -e

cmd="$@"

until curl --fail http://ipfs:5001/api/v0/id; do
  >&2 echo "IPFS cluster is unavailable - sleeping"
  sleep 1
done

until curl --fail http://ipfs-cluster:9094/id; do
  >&2 echo "IPFS cluster is unavailable - sleeping"
  sleep 1
done

exec $cmd

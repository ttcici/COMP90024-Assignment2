#!/bin/bash

echo "== Add nodes (slave1) to cluster =="
curl -X POST -H "Content-Type: application/json" http://user:pass@172.26.133.141:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "user", "password":"pass", "port": 5984, "node_count": "3", "remote_node": "172.26.133.82", "remote_current_user": "user", "remote_current_password": "pass" }'
curl -X POST -H "Content-Type: application/json" http://user:pass@172.26.133.141:5984/_cluster_setup -d '{"action": "add_node", "host":"172.26.133.82", "port": 5984, "username": "user", "password":"pass"}'

echo "== Add nodes (slave2) to cluster =="
curl -X POST -H "Content-Type: application/json" http://user:pass@172.26.133.141:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "user", "password":"pass", "port": 5984, "node_count": "3", "remote_node": "172.26.134.37", "remote_current_user": "user", "remote_current_password": "pass" }'
curl -X POST -H "Content-Type: application/json" http://user:pass@172.26.133.141:5984/_cluster_setup -d '{"action": "add_node", "host":"172.26.134.37", "port": 5984, "username": "user", "password":"pass"}'

echo "== Complete cluster setup =="
curl -X POST -H "Content-Type: application/json" http://user:pass@172.26.133.141:5984/_cluster_setup -d '{"action": "finish_cluster"}'

curl http://user:pass@172.26.133.141:5984/_membership
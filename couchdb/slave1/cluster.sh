
#!/bin/bash

echo "== Add nodes to cluster =="
curl -X POST -H "Content-Type: application/json" http://user:pass@172.26.37.244:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "user", "password":"pass", "port": 5984, "node_count": "2", "remote_node": "172.26.38.15", "remote_current_user": "user", "remote_current_password": "pass" }'
curl -X POST -H "Content-Type: application/json" http://user:pass@172.26.37.244:5984/_cluster_setup -d '{"action": "add_node", "host":"172.26.38.15", "port": 5984, "username": "user", "password":"pass"}'
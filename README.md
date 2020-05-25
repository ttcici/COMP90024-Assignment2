# COMP90024-Assignment2

# Project Structure
Deployment

  1. Ansible creates and configures 4 instances at once
  2. Ansible clones the code from team's GitHub repository
  3. Ansible runs the docker-compose.yaml to deploy CouchDB nodes, data harvester, web server and backend code
  
Server Arrangement

  instance-1: 172.26.132.129
  > Backend/ 
  
  > Frontend/
  
  > COMP90024/
  
  instance-2: 172.26.133.141, instance-3: 172.26.133.82 and instance-4: 172.26.134.37
  > CouchDB/
  
  > Data Harvester/
  
  > COMP90024/

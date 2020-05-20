#!/bin/bash
. ./unimelb-comp90024-2020-grp-16-openrc.sh; ansible-playbook -i hosts --ask-become-pass full-stack.yaml
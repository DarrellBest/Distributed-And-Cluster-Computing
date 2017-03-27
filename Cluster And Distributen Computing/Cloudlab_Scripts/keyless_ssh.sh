#!/bin/sh

ssh-keygen -t rsa -P "" -f "~/.ssh"
cd ~/.ssh
cp id_rsa.pub authorized_keys
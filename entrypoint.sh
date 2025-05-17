#!/bin/sh

# Ensure /etc/environment exists
touch /etc/environment

# Export only AWS-related variables to system-wide environment
printenv | grep '^AWS_' >> /etc/environment

# Start SSH daemon in foreground
exec /usr/sbin/sshd -D
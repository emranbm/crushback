#!/usr/bin/env sh
# This script is used to provide socks proxy for docker-compose services.

set -eu

if [ "$SOCKS_HOST" = "" ]; then
  echo "Warning: Running a fake proxy to the local (i.e. no proxy) since the SOCKS_HOST variable is empty."
  echo "Configuring sshd ..."
  echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
  echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
  /usr/bin/ssh-keygen -A
  /usr/sbin/sshd
  echo "root:123" | chpasswd
  echo "Proxying traffic to this container itself! ..."
  sshpass -p "123" ssh -oServerAliveInterval=100 -oStrictHostKeyChecking=no -D ":9000" -N root@localhost
else
  echo "Proxying to $SOCKS_HOST ..."
  sshpass -p "$SOCKS_PASS" ssh -oServerAliveInterval=100 -oStrictHostKeyChecking=no -D ":9000" -N "$SOCKS_USER@$SOCKS_HOST"
fi

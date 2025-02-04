#!/bin/sh

# Start the proxy service.

set -e

# Put our config file where nginx expects it and substitute the env
# vars (at runtime).
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# Run nginx in the foreground (since it is run in a separate Docker container).
nginx -g 'daemon off;'

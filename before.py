import os
from subprocess import run
from deployment import prepare_deployment

ZROK_TOKEN = os.getenv('ZROK_TOKEN')
UPSTREAM_NAME = os.getenv('UPSTREAM_NAME')

# Prepare deployment
prepare_deployment()

# Enable zrok environment
run(['zrok', 'enable', ZROK_TOKEN, '-d', UPSTREAM_NAME])

# Reserve a domain name
run(['zrok', 'reserve', 'public', 'localhost:8001', '-n', UPSTREAM_NAME])

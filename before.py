import os
import requests
import uuid
import dotenv

# Load environmental variables
RUBECTL_API = os.getenv('RUBECTL_API')

# Load deployment from the API
resp = requests.get(f'{RUBECTL_API}/api/v1/deployments/weakest')
resp.raise_for_status()
deployment = resp.json()['data']

# Generate upstream name and url
upstream_name = str(uuid.uuid4()).replace('-', '').strip()[:8]
upstream_url = f'https://{upstream_name}.share.zrok.io'

# Add information to docker compose
with open('docker-compose.yml', 'r', encoding='utf-8') as f:
    docker_compose = f.read()
    docker_compose = docker_compose.replace('${DEPLOYMENT_IMAGE}', deployment['image'])
    docker_compose = docker_compose.replace('${UPSTREAM_NAME}', upstream_name)
with open('docker-compose.yml', 'w', encoding='utf-8') as f:
    f.write(docker_compose)

# Save environmental variables
open('.env', 'x', encoding='utf-8').close()
dotenv.set_key('.env', 'DEPLOYMENT_UUID', deployment['uuid'])
dotenv.set_key('.env', 'UPSTREAM_NAME', upstream_name)
dotenv.set_key('.env', 'UPSTREAM_URL', upstream_url)

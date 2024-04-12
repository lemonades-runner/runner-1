import os
import time
import subprocess
import requests
import dotenv

# Load environmental variables
dotenv.load_dotenv()
LIFETIME = os.getenv('LIFETIME')
UPSTREAM_NAME = os.getenv('UPSTREAM_NAME')
UPSTREAM_URL = os.getenv('UPSTREAM_URL')
RUBECTL_API = os.getenv('RUBECTL_API')
DEPLOYMENT_UUID = os.getenv('DEPLOYMENT_UUID')

# Setup pod lifetime
if LIFETIME:
    LIFETIME = int(LIFETIME)
else:
    LIFETIME = 3 * 60 * 60  # 3 hours lifetime by default

# Save upstream to the API
resp = requests.post(f'{RUBECTL_API}/api/v1/upstreams', json={
    'deployment_uuid': DEPLOYMENT_UUID,
    'url': UPSTREAM_URL
})
resp.raise_for_status()
resp = resp.json()['data']

# Wait until death
for i in range(LIFETIME):
    time.sleep(1)
    print(f'Alive: {i + 1}/{LIFETIME}')

# Release the domain name
subprocess.run(['zrok', 'release', UPSTREAM_NAME])

# Disable zrok environment
subprocess.run(['zrok', 'disable'])

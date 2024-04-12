import os
from time import sleep
from subprocess import run
from upstream import prepare_upstream
from dotenv import load_dotenv

# Get pod lifetime
LIFETIME = os.getenv('LIFETIME')
if LIFETIME:
    LIFETIME = int(LIFETIME)
else:
    LIFETIME = 3 * 60 * 60  # 3 hours lifetime by default

load_dotenv()

# Share the upstream
UPSTREAM_NAME = os.getenv('UPSTREAM_NAME')
run(['zrok', 'share', 'reserved', UPSTREAM_NAME])

# Notify Rubectl about the upstream
prepare_upstream()

# Wait until death
for i in range(LIFETIME):
    sleep(1)
    print(f'Alive: {i + 1}/{LIFETIME}')

# Release the domain name
run(['zrok', 'release', UPSTREAM_NAME])

# Disable zrok environment
run(['zrok', 'disable'])

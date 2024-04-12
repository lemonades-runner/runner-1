import os
from requests import post


def prepare_upstream():
    RUBECTL_API = os.getenv('RUBECTL_API')
    DEPLOYMENT_UUID = os.getenv('DEPLOYMENT_UUID')
    UPSTREAM_URL = os.getenv('UPSTREAM_URL')

    resp = post(f'{RUBECTL_API}/api/v1/upstreams', json={
        'deployment_uuid': DEPLOYMENT_UUID,
        'url': UPSTREAM_URL
    })

    if resp.status_code == 200:
        resp = resp.json()
        print(resp)
        return True

    print(resp.text)
    return False

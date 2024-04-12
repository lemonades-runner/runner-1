import os
from requests import get
from uuid import uuid4
from dotenv import load_dotenv


def prepare_deployment():
    RUBECTL_API = os.getenv('RUBECTL_API')
    resp = get(f'{RUBECTL_API}/api/v1/deployments/weakest')
    if resp.status_code == 200:
        deployment = resp.json()['data']
        upstream_name = str(uuid4()).replace('-', '').strip()[:6]
        upstream_url = f'https://{upstream_name}.share.zrok.io'
        with open('.env', 'w', encoding='utf-8') as f:
            envs = (f"DEPLOYMENT_UUID={deployment['uuid']}\n"
                    f"DEPLOYMENT_IMAGE={deployment['image']}\n"
                    f"UPSTREAM_NAME={upstream_name}\n"
                    f"UPSTREAM_URL={upstream_url}\n")
            print('Successfully fetched envs:')
            print(envs)
            f.write(envs)

        # Adding deployment image to docker compose
        with open('docker-compose.yml', 'r', encoding='utf-8') as f:
            docker_compose = f.read().replace('${PROXY_IMAGE}', deployment['image'])
        with open('docker-compose.yml', 'w', encoding='utf-8') as f:
            f.write(docker_compose)

        load_dotenv()
        return True

    print(resp.text)
    return False

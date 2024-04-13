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


def publication_is_ready(attempts: int = 10):
    """
    Checks if the publication is ready.
    :param attempts: count of attempts to check the publication is ready.
    :return: is_ready: bool.
    """
    for i in range(10):
        try:
            if requests.get(f'{UPSTREAM_URL}/healthz').status_code == 200:
                print('Publication available.')
                return True
        except Exception as e:
            print(e)
        print(f'Publication unavailable. Attempt: {i}/{attempts}.')
        time.sleep(3)
    print('Publication unavailable. No more attempts.')
    return False


def post_upstream():
    """
    Save upstream to the API.
    :return:
    """
    resp = requests.post(f'{RUBECTL_API}/api/v1/upstreams', json={
        'deployment_uuid': DEPLOYMENT_UUID,
        'url': UPSTREAM_URL
    })
    resp.raise_for_status()
    return resp.json()['data']


def live():
    """
    Wait until death.
    :return:
    """
    for i in range(LIFETIME):
        time.sleep(1)
        if i % LIFETIME // 100 == 0:
            print(f'Alive: {i + 1}/{LIFETIME}', flush=True)


def publication_finish():
    """
    Releases the domain name and disables the environment.
    :return:
    """
    # Release the domain name
    subprocess.run(['zrok', 'release', UPSTREAM_NAME])
    # Disable zrok environment
    subprocess.run(['zrok', 'disable'])


def main():
    if publication_is_ready():
        post_upstream()
        live()
    # publication_finish()  # no zrok here so this should be in docker


if __name__ == '__main__':
    main()

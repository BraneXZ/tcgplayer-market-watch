import logging
import requests

from decouple import config


def request_access_token():
    """Update access token if expired"""

    # See if access token is still functioning
    USER_AGENT = config('USER_AGENT')

    try:
        with open('.access_token', 'r') as f:
            access_token = f.read()
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            'User-Agent': USER_AGENT,
            "Authorization": "bearer " + access_token}
        url = "https://api.tcgplayer.com/catalog/categories"
        response = requests.get(url, headers=headers)

        logging.info(response.json())
        if not response.json()['success']:
            raise Exception

    except Exception:
        logging.info('Access token expired or does not exist')

        TCG_PUBLIC_KEY = config('TCG_PUBLIC_KEY')
        TCG_PRIVATE_KEY = config('TCG_PRIVATE_KEY')

        response = requests.post(
            "https://api.tcgplayer.com/token",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"},

            data=(f"grant_type=client_credentials"
                  f"&client_id={TCG_PUBLIC_KEY}&"
                  f"client_secret={TCG_PRIVATE_KEY}")
        )
        logging.info("Received access_token")

        # access_token = response.json()['access_token']
        access_token = 'abc'
        with open('.access_token', 'w') as f:
            logging.info("Writing access token to file .access_token")
            f.write(access_token)

    return access_token


if __name__ == '__main__':
    logging.basicConfig(filename='.log', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s %(levelname)-8s %(message)s')

    access_token = request_access_token()

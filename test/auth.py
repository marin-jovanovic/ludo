import json
import random
import requests


def create_user(u,p):
    url = "http://localhost:8000/signup"

    t = requests.post(
        f"{url}/{u}",
        headers= {
            'password': p
        },
        data={
            # "portfolio": portfolio
        },
        verify=False
    )

    print(json.dumps(json.loads(t.text), indent=4, sort_keys=True))


def main():
    print('running tests')
    create_user('username1', 'password1')

if __name__ == '__main__':
    main()
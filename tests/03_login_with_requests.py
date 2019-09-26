import requests
from http import HTTPStatus

USERNAME = 'admin'
PASSWORD = 'default'

response = requests.post(url='http://0.0.0.0:5000/login',
                         data={'username': USERNAME,
                               'password': PASSWORD},
                         allow_redirects=False
                         )

for c in response.cookies:
    print(c.name, c.value)

assert response.status_code == HTTPStatus.FOUND
assert 'session' in response.cookies.keys()

import requests
from http import HTTPStatus


# Constants
URL = "http://0.0.0.0:5000/"
USERNAME = 'admin'
PASSWORD = 'default'

# Send request to web server to mimic login page form submission
response = requests.post(url=f"{URL}login",
                         data={'username': USERNAME,
                               'password': PASSWORD},
                         allow_redirects=False
                         )

# Print all received cookies that are send by server
for c in response.cookies:
    print(c.name, c.value)

# Verify response status code
assert response.status_code == HTTPStatus.FOUND

# Verify that cookie with session token has been received
assert 'session' in response.cookies.keys()

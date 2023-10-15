![Python versions](https://img.shields.io/badge/python-3.9-blue.svg)



# CTFd Unique User Token Plugin

This plugin for CTFd generates a unique token for each user and provides functionality to replace certain placeholders on the client-side with that token. It also introduces a mechanism to automatically submit challenges using these tokens.

## Features

- Generates a secure and unique token for each registered user in CTFd.
- Automatically replaces the `##unique_token##` placeholder in challenge descriptions with the user's token.
- Provides an API route for admins to solve challenges on behalf of a user using their token.

## Installation

1. Clone this repository into your CTFd's plugins directory:

```bash
cd /path/to/CTFd/plugins
git clone [REPOSITORY_URL]
```

2. Restart CTFd or your web server.

3. Configure the environment variables `UNIQUE_TOKEN_SECRETKEY` and `UNIQUE_TOKEN_SALT` to enhance the security of the generated tokens.

## Usage

Once installed, the plugin will automatically generate a token for each user upon logging in. Moreover, any instance of `##unique_token##` in challenge descriptions will be replaced with the user's unique token.


### API

- **GET** `/get_user_token`: Retrieves the current user's token.
- **GET** `/admin-solve/<token>/<challenge_name>`: Solves a challenge for a user using their token (admin only). Example:
  - ADMIN_TOKEN: Generate it in `https://CTFD/settings#tokens`
  - CTFD: CTFD URL

curl: 
```bash
curl  'http://<CTFD>/admin-solve/<USER_UNIQUE_TOKEN>/<CHALLENGE_FULL_NAME>' -H 'Authorization: Token <ADMIN_CTFD_TOKEN>' -H 'Content-type: application/json'
```

Python: 
```py
import requests

def request_to_ctfd(url, admin_ctfd_token, user_unique_token, challenge_name):
    r = requests.get(f"{url}/admin-solve/{user_unique_token}/{challenge_name}", headers={'Content-Type':'application/json', 'Authorization': f"Bearer {admin_ctfd_token}"})
    return(r.text)
```


## Contributions

Contributions are welcome. Please create an issue or pull request if you find a bug or wish to add a new feature.


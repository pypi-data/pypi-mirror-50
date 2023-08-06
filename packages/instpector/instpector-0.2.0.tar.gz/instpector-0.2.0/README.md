# Instpector

A simple Instagram's web API library written in Python. No selenium or webdriver required. 

Login with two-factor authentication enabled is supported.

# Installation

```
pip install instpector
```

# Sample usage

```python
from instpector import Instpector, endpoints

instpector = Instpector()

# Login into Instagram's web
instpector.login("my_username", "my_password")

# Get the profile of any user, for example 'some_username'
profile = endpoints.factory.create("profile", instpector)
insta_profile = profile.of_user("some_username")
print(insta_profile)
# id, followers_count, following_count, is_private, ... 

# Iterate all followers of 'some_username'
followers = endpoints.factory.create("followers", instpector)
for follower in followers.of_user(insta_profile.id):
    print(follower)
    # id, username, full_name, ...

# Logout
instpector.logout()
```

## Using 2FA
For login in using two-factor authentication, generate your 2fa key on Instagram's app and provide the code when logging in with `instpector`. The following example uses `pytop` to demonstrate the usage:

```python
from pyotp import TOTP
from instpector import Instpector, endpoints

instpector = Instpector()
totp = TOTP("my_2fa_key") # Input without spaces

# Login into Instagram's web
instpector.login("my_username", "my_password", totp.now())
```

Check more in the `examples` directory.

# Available endpoints

- Followers   
- Following   
- Timeline   
- Profile   
- Story Reel    
- Story    

More to come

# Development dependencies

- requests

# Tests

1. Create a `pytest.ini` file with the sample contents of  `pytest.sample.ini` in the `tests` directory.

2. Add your account information. 
3. Run with `pytest`:
```
(env)$ pytest -qs tests
```

# Disclaimer

This tool is not affiliated with, authorized, maintained or endorsed by Instagram or any of its affiliates or subsidiaries. Use at your own risk.

# License

Licensed under MIT License.
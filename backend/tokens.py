from datetime import datetime, timezone, timedelta

from jwt import encode, decode
from os import getenv

## Helps with callers not having to deal with raw json
class jwt_result:
    uid: int
    success: bool

    def __init__(self, success: bool, uid: int = -1):
        self.success = success
        self.uid = uid

#https://pyjwt.readthedocs.io/en/stable/usage.html

## Confirm a user login token was signed using
## The server's secret key. Also returns
## false if it's expired etc...
def confirm_jwt(token) -> jwt_result:
    private_key: str = getenv("JWT_SECRET_KEY")
    try:
        result = decode(
            token,
            private_key,
            options={"require": ["exp", "sub", "iat"]}, # require everything we set in create_jwt
            algorithms=["HS256"],
        )

        uid = result.get("sub")

        return jwt_result(True, int(uid))
    except Exception as e:
        print("Could not authenticate token: " + str(e))
        return jwt_result(False)

## Sign a new JWT using the server's secret key
## returns a dictionary ready to jsonify 
def create_jwt(user_id: int, expiration_days_from_now: int = 1) -> dict:
    private_key: str = getenv("JWT_SECRET_KEY")
    try:
        result = encode(
            {
                "sub": str(user_id), # Unique identifier
                "exp": datetime.now(tz=timezone.utc) + 
                timedelta(days=expiration_days_from_now), # expiration time
                "iat": datetime.now(tz=timezone.utc) # for debugging: time of creation
            },
            private_key,
            algorithm="HS256",
        )
        return result
    except Exception as e:
        print("Could not generate token! " + str(e))
        return None
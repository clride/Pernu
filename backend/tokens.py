from datetime import datetime, timezone, timedelta

from jwt import encode, decode
from os import getenv

class jwt_result:
    uid: int
    success: bool

    def __init__(self, success: bool, uid: int = -1):
        self.success = success
        self.uid = uid

#https://pyjwt.readthedocs.io/en/stable/usage.html
def confirm_jwt(token) -> jwt_result:
    private_key: str = getenv("JWT_SECRET_KEY")
    try:
        result = decode(
            token,
            private_key,
            options={"require": ["exp", "sub", "iat"]},
            algorithms=["HS256"],
        )

        uid = result.get("sub")

        return jwt_result(True, uid)
    except Exception as e:
        print("Could not authenticate token: " + str(e))
        return jwt_result(False)
    
def create_jwt(user_id: int, expiration_days_from_now: int = 1) -> dict:
    private_key: str = getenv("JWT_SECRET_KEY")
    try:
        result = encode(
            {
                "sub": str(user_id),
                "exp": datetime.now(tz=timezone.utc) + 
                timedelta(days=expiration_days_from_now),
                "iat": datetime.now(tz=timezone.utc)
            },
            private_key,
            algorithm="HS256",
        )
        return result
    except Exception as e:
        print("Could not generate token! " + str(e))
        return None
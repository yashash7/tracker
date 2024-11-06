import base64
from datetime import datetime, timedelta, timezone
from fastapi import Header
from fastapi.responses import JSONResponse, RedirectResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as interceptor_req
from typing import Optional
from .utils import get_env_var

psd_context = CryptContext(schemes=[get_env_var("psd_hash_scheme")], deprecated="auto")

def create_psd(psd: str) -> str:
    psd = base64.b64decode(psd).decode(get_env_var("default_charset"))
    return psd_context.hash(psd)

def verify_psd(given_psd: str, original_psd: str) -> bool:
    return psd_context.verify(given_psd, original_psd)

''' JWT Utils '''
SECRET_KEY = get_env_var("jwt_secret_key")
ALGORITHM = get_env_var("jwt_algorithm")
ACCESS_TOKEN_EXPIRY = int(get_env_var("access_token_expiry")) #in minutes

# create jwt token for an user
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY)
    expire = expire.isoformat()
    data_to_encode.update({"expiry": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# verify jwt token of an user
def verify_access_token(Authorization: Optional[str] = Header(None)) -> dict:
    try:
        payload = jwt.decode(Authorization, SECRET_KEY, algorithms=[ALGORITHM])
        response = payload
    except JWTError:
        response = None
    return response

# Authentication Interceptor
class Interceptor(BaseHTTPMiddleware):
    
    def __init__(self, app):
        super().__init__(app)
        self.public_routes = get_env_var("public_routes")
        self.app_routes = getattr(getattr(self.app, "app"), "routes")
        
    async def dispatch(self, request: interceptor_req, call_next):
        # Code that runs before the request reaches the route
        end_point = request.url.path
        print("Intercepted \"" + end_point + "\"")
        # Check valid path and redirect back to home if invalid
        if not any(getattr(app_route, "path") == end_point for app_route in self.app_routes):
            return RedirectResponse("/")
        # Check for authorization
        auth_token = request.headers.get("authorization")
        if end_point not in self.public_routes and not auth_token:
            response = JSONResponse(status_code=401, content="Please Login to Access this Resource!")
        elif end_point not in self.public_routes and not verify_access_token(auth_token):
            response = JSONResponse(status_code=401, content="Session Expired, Please Login Again!")
        else:
            response = await call_next(request)
        return response
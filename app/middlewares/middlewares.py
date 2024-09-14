from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import jwt # type: ignore

SECRET_KEY = "57168498522b9b42531f34be15dcd8d7e1a5fe14261c7d80e82cb9cdac26bd6b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("access_token")
        if token:
            try:
                token = token.replace("Bearer ", "")
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                request.state.user = payload.get("sub")
            except jwt.ExpiredSignatureError:
                request.state.user = None
            except jwt.InvalidTokenError:
                request.state.user = None
            except Exception as e:
                request.state.user = None
                print(f"Error decoding JWT: {e}")
        else:
            request.state.user = None

        try:
            response = await call_next(request)
        except Exception as e:
            print(f"Error in call_next: {e}")
            response = JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)
        
        return response


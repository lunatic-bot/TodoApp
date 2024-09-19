from starlette.middleware.base import BaseHTTPMiddleware  # Import base class for creating custom middleware
from starlette.requests import Request  # Import Request class to handle incoming requests
from starlette.responses import JSONResponse  # Import JSONResponse to handle error responses
import jwt  # type: ignore # Import JWT for token decoding and validation

# JWT settings
SECRET_KEY = "57168498522b9b42531f34be15dcd8d7e1a5fe14261c7d80e82cb9cdac26bd6b"  # Secret key for signing JWTs
ALGORITHM = "HS256"  # Algorithm used to sign and verify JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time

# Custom middleware class for handling JWT tokens
class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Middleware function to extract and decode JWT tokens from cookies
        before passing the request to the next handler.
        """
        token = request.cookies.get("access_token")  # Get the token from cookies
        if token:
            try:
                token = token.replace("Bearer ", "")  # Remove 'Bearer ' from the token if present
                # Decode the token using the secret key and algorithm
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                # Extract the 'sub' (subject) field from the token payload and store it in the request state
                request.state.user = payload.get("sub")
            except jwt.ExpiredSignatureError:  # Handle expired tokens
                request.state.user = None
            except jwt.InvalidTokenError:  # Handle invalid tokens
                request.state.user = None
            except Exception as e:  # Handle any other exceptions during token decoding
                request.state.user = None
                print(f"Error decoding JWT: {e}")  # Log the error for debugging
        else:
            # If no token is found, set the user state to None
            request.state.user = None

        try:
            # Pass the request to the next middleware or endpoint
            response = await call_next(request)
        except Exception as e:  # Handle any exceptions from the next handler
            print(f"Error in call_next: {e}")  # Log the error for debugging
            # Return a JSON response with a 500 status code in case of an internal server error
            response = JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)
        
        return response  # Return the response from the next middleware or endpoint

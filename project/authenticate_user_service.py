from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class AuthenticationResponse(BaseModel):
    """
    The response model for authentication attempts. It includes the OAuth token if authentication is successful or an error message otherwise.
    """

    success: bool
    oauth_token: Optional[str] = None
    error_message: Optional[str] = None


async def authenticate_user(username: str, password: str) -> AuthenticationResponse:
    """
    Authenticates a user and returns an OAuth token.

    Args:
    username (str): The username of the user attempting to authenticate.
    password (str): The password of the user attempting to authenticate. It should be transmitted over a secure connection and stored securely.

    Returns:
    AuthenticationResponse: The response model for authentication attempts. It includes the OAuth token if authentication is successful or an error message otherwise.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return AuthenticationResponse(
            success=True, oauth_token="simulated_oauth_token_for_" + username
        )
    else:
        return AuthenticationResponse(
            success=False,
            error_message="Authentication failed. Wrong username or password.",
        )

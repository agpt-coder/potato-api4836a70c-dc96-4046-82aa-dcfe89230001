from typing import Optional

import prisma
import prisma.models
from bcrypt import gensalt, hashpw
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    Model for the response returned upon the successful creation of a new user account. Includes user ID and confirmation message.
    """

    user_id: str
    message: str


async def create_user(
    email: str, password: str, username: Optional[str] = None
) -> CreateUserResponse:
    """
    Creates a new user account with an email, password, and an optional username. The password is hashed before storing in the database.

    Args:
    email (str): The email address for the new user. It must be unique.
    password (str): The password for the new user. This will be hashed before storing in the database.
    username (Optional[str]): An optional username for the user. This can be used as an alternative identifier for the user.

    Returns:
    CreateUserResponse: Model for the response returned upon the successful creation of a new user account. Includes user ID and confirmation message.

    Example:
    create_user('test@example.com', 'securepassword', 'testuser')
    > CreateUserResponse(user_id='...', message='prisma.models.User created successfully.')
    """
    hashed_password = hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")
    user_data = {"email": email, "password": hashed_password}
    if username:
        user_data["username"] = username
    user = await prisma.models.User.prisma().create(data=user_data)
    return CreateUserResponse(
        user_id=user.id, message="prisma.models.User created successfully."
    )

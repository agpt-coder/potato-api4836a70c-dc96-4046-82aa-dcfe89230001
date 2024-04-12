from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ValidateAPIKeyResponse(BaseModel):
    """
    Response model indicating whether the API key is valid along with corresponding user details, if authenticated.
    """

    is_valid: bool
    user_id: Optional[str] = None
    message: str


async def validate_api_key(api_key: str) -> ValidateAPIKeyResponse:
    """
    Validates an API key for third-party service access.

    This function checks in the database whether the provided API key is valid and, if so, fetches the user ID associated with this key.

    Args:
    api_key (str): The API key to be validated.

    Returns:
    ValidateAPIKeyResponse: Response model indicating whether the API key is valid along with corresponding user details, if authenticated.

    Example:
        validate_api_key("valid-api-key-string")
        > ValidateAPIKeyResponse(is_valid=True, user_id="some-user-id", message="API key is valid.")

        validate_api_key("invalid-api-key-string")
        > ValidateAPIKeyResponse(is_valid=False, user_id=None, message="Invalid API key.")
    """
    api_key_record = await prisma.models.ApiKey.prisma().find_unique(
        where={"key": api_key}, include={"user": True}
    )
    if api_key_record:
        return ValidateAPIKeyResponse(
            is_valid=True, user_id=api_key_record.user.id, message="API key is valid."
        )
    else:
        return ValidateAPIKeyResponse(
            is_valid=False, user_id=None, message="Invalid API key."
        )

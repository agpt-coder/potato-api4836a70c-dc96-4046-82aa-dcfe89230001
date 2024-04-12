#     "pydantic.main.BaseModel" is incompatible with "code.BaseModel"
#     Type "type[pydantic.main.BaseModel]" cannot be assigned to type "type[code.BaseModel]". reportAssignmentType
from typing import Optional

import prisma
import prisma.models
from pydantic import (
    BaseModel,
)  # TODO(autogpt): Expression of type "type[pydantic.main.BaseModel]" cannot be assigned to declared type "type[code.BaseModel]"


class UpdatedUserDetails(BaseModel):
    """
    A model representing the updated user account information for confirmation purposes.
    """

    username: str
    email: str
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None


class UpdateUserResponse(BaseModel):
    """
    Provides feedback on the update process, including confirmation of the update or relevant error messages.
    """

    success: bool
    message: str
    updated_user_details: UpdatedUserDetails


class BaseModel:
    pass


async def update_user(
    id: str,
    username: str,
    email: str,
    bio: Optional[str],
    profile_image_url: Optional[str],
) -> UpdateUserResponse:
    """
    Updates an existing user's account information.

    Args:
        id (str): The unique identifier of the user whose account information needs to be updated.
        username (str): The new username for the user.
        email (str): The new email address for the user.
        bio (Optional[str]): A short bio or description about the user.
        profile_image_url (Optional[str]): URL to the user's new profile image.

    Returns:
        UpdateUserResponse: Provides feedback on the update process, including confirmation of the update or relevant error messages.
    """
    try:
        user = await prisma.models.User.prisma().find_unique(where={"id": id})
        if user:
            updated_user = await prisma.models.User.prisma().update(
                where={"id": id}, data={"email": email}
            )
            return UpdateUserResponse(
                success=True,
                message="User updated successfully.",
                updated_user_details=UpdatedUserDetails(
                    username=username,
                    email=updated_user.email,
                    bio=bio,
                    profile_image_url=profile_image_url,
                ),
            )  # TODO(autogpt): Expected no arguments to "UpdateUserResponse" constructor. reportCallIssue
        else:
            return UpdateUserResponse(
                success=False, message="User not found."
            )  # TODO(autogpt): Expected no arguments to "UpdateUserResponse" constructor. reportCallIssue
    except Exception as e:
        return UpdateUserResponse(
            success=False, message=f"Failed to update user: {e}"
        )  # TODO(autogpt): Expected no arguments to "UpdateUserResponse" constructor. reportCallIssue

import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    This response model indicates the result of the deletion process.
    """

    success: bool
    message: str


async def delete_user(id: str) -> DeleteUserResponse:
    """
    Deletes a user account.

    This function involves connecting to the database using the Prisma client and deleting a user record based on the provided unique identifier.
    After attempting to delete the user, it returns a response that signifies whether the deletion was successful,
    along with a message providing feedback on the deletion process.

    Args:
    id (str): The unique identifier of the user account to be deleted.

    Returns:
    DeleteUserResponse: This response model indicates the result of the deletion process with a success flag and a human-readable message.
    """
    try:
        user = await prisma.models.User.prisma().delete(where={"id": id})
        return DeleteUserResponse(
            success=True, message="prisma.models.User deleted successfully."
        )
    except Exception as e:
        return DeleteUserResponse(
            success=False,
            message="An error occurred while deleting the user. {}".format(str(e)),
        )

import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.authenticate_user_service
import project.create_user_service
import project.delete_user_service
import project.fetch_random_photo_service
import project.update_user_service
import project.validate_api_key_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="potato api",
    lifespan=lifespan,
    description="To create a Potato API that takes in any input/API call and returns a photo of a potato, here's a comprehensive plan based on the functionality expectations and the tech stack specified:\n\n1. **Tech Stack**:\n- **Programming Language**: Python\n- **API Framework**: FastAPI\n- **Database**: PostgreSQL\n- **ORM**: Prisma\n\n2. **Functionality**:\n- The API should accept any input through an API call and respond with a random photo of a potato.\n\n3. **Implementation Steps**:\n- **Database Setup**: Utilize PostgreSQL to store information about the potato photos. This might include URLs to the actual files stored in a cloud service like AWS S3.\n- **Prisma Setup**: Use Prisma as the ORM to interact with the PostgreSQL database. Define a model for the potato photos that includes fields for ID, URL, and any other relevant metadata.\n- **Fetching Random Photos**: Implement a method to fetch a random photo URL from the database. This could involve generating a random index or using a PostgreSQL function to randomly select a row.\n- **FastAPI Endpoint**: Create an endpoint in FastAPI that handles incoming requests. Upon a request, the endpoint should trigger the method to fetch a random potato photo and return the photo's URL to the requester.\n- **Static File Storage**: Store the actual potato photos in a cloud service, such as AWS S3. Ensure each photo has a unique URL which is stored in the PostgreSQL database.\n- **Error Handling**: Implement error handling to manage cases where the photo cannot be retrieved or the database is unreachable.\n\n4. **Security and Performance Considerations**:\n- Implement rate limiting and authentication as necessary to prevent abuse.\n- Consider using CDN for serving photos to enhance load times and reduce bandwidth usage.\n\nThis plan leverages the indicated tech stack and the details gathered through the interview process, aiming to fulfill the requirement of delivering a random potato photo in response to any API call. The API will be built with scalability and efficiency in mind, ensuring a smooth user experience.",
)


@app.delete("/user/{id}", response_model=project.delete_user_service.DeleteUserResponse)
async def api_delete_delete_user(
    id: str,
) -> project.delete_user_service.DeleteUserResponse | Response:
    """
    Deletes a user account.
    """
    try:
        res = await project.delete_user_service.delete_user(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/photos/random",
    response_model=project.fetch_random_photo_service.PhotoResponseModel,
)
async def api_get_fetch_random_photo() -> project.fetch_random_photo_service.PhotoResponseModel | Response:
    """
    Fetches a random potato photo's URL from the database.
    """
    try:
        res = await project.fetch_random_photo_service.fetch_random_photo()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/auth/validate",
    response_model=project.validate_api_key_service.ValidateAPIKeyResponse,
)
async def api_get_validate_api_key(
    api_key: str,
) -> project.validate_api_key_service.ValidateAPIKeyResponse | Response:
    """
    Validates an API key for third-party service access.
    """
    try:
        res = await project.validate_api_key_service.validate_api_key(api_key)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/login",
    response_model=project.authenticate_user_service.AuthenticationResponse,
)
async def api_post_authenticate_user(
    username: str, password: str
) -> project.authenticate_user_service.AuthenticationResponse | Response:
    """
    Authenticates a user and returns an OAuth token.
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(
            username, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/user", response_model=project.create_user_service.CreateUserResponse)
async def api_post_create_user(
    email: str, password: str, username: Optional[str]
) -> project.create_user_service.CreateUserResponse | Response:
    """
    Creates a new user account.
    """
    try:
        res = await project.create_user_service.create_user(email, password, username)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put("/user/{id}", response_model=project.update_user_service.UpdateUserResponse)
async def api_put_update_user(
    id: str,
    username: str,
    email: str,
    bio: Optional[str],
    profile_image_url: Optional[str],
) -> project.update_user_service.UpdateUserResponse | Response:
    """
    Updates an existing user's account information.
    """
    try:
        res = await project.update_user_service.update_user(
            id, username, email, bio, profile_image_url
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )

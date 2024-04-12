from random import randint

import prisma
import prisma.models
from pydantic import BaseModel


class PhotoResponseModel(BaseModel):
    """
    This response model contains the URL of the randomly selected potato photo, retrieved from the database.
    """

    photo_url: str


async def fetch_random_photo() -> PhotoResponseModel:
    """
    Fetches a random potato photo's URL from the database.

    Returns:
    PhotoResponseModel: This response model contains the URL of the randomly selected potato photo,
                        retrieved from the database.
    """
    total_photos = await prisma.models.Photo.prisma().count()
    if total_photos == 0:
        raise Exception("No photos available in the database.")
    random_index = randint(0, total_photos - 1)
    photo = await prisma.models.Photo.prisma().find_many(skip=random_index, take=1)
    if not photo:
        raise Exception("Failed to fetch a random photo.")
    photo_url = photo[0].url
    return PhotoResponseModel(photo_url=photo_url)

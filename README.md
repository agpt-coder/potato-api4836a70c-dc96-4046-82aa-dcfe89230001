---
date: 2024-04-12T17:12:29.133996
author: AutoGPT <info@agpt.co>
---

# potato api

To create a Potato API that takes in any input/API call and returns a photo of a potato, here's a comprehensive plan based on the functionality expectations and the tech stack specified:

1. **Tech Stack**:
- **Programming Language**: Python
- **API Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: Prisma

2. **Functionality**:
- The API should accept any input through an API call and respond with a random photo of a potato.

3. **Implementation Steps**:
- **Database Setup**: Utilize PostgreSQL to store information about the potato photos. This might include URLs to the actual files stored in a cloud service like AWS S3.
- **Prisma Setup**: Use Prisma as the ORM to interact with the PostgreSQL database. Define a model for the potato photos that includes fields for ID, URL, and any other relevant metadata.
- **Fetching Random Photos**: Implement a method to fetch a random photo URL from the database. This could involve generating a random index or using a PostgreSQL function to randomly select a row.
- **FastAPI Endpoint**: Create an endpoint in FastAPI that handles incoming requests. Upon a request, the endpoint should trigger the method to fetch a random potato photo and return the photo's URL to the requester.
- **Static File Storage**: Store the actual potato photos in a cloud service, such as AWS S3. Ensure each photo has a unique URL which is stored in the PostgreSQL database.
- **Error Handling**: Implement error handling to manage cases where the photo cannot be retrieved or the database is unreachable.

4. **Security and Performance Considerations**:
- Implement rate limiting and authentication as necessary to prevent abuse.
- Consider using CDN for serving photos to enhance load times and reduce bandwidth usage.

This plan leverages the indicated tech stack and the details gathered through the interview process, aiming to fulfill the requirement of delivering a random potato photo in response to any API call. The API will be built with scalability and efficiency in mind, ensuring a smooth user experience.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'potato api'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow

# Face Locker Backend

This repository contains the Face Locker backend (FastAPI) with support for local, AWS S3 and Azure Blob storage,
plus an in-memory cache for recognizer models (auto-reloads after training, add-user, or delete-user).

## Structure

- app/ - FastAPI application and service code
- Front-locker-patch/ - example changes to Front-locker.py to send Authorization header
- requirements.txt
- Dockerfile

## Environment variables

- STORAGE_BACKEND: local | s3 | azure (default: local)
- DATASET_DIR: local path when STORAGE_BACKEND=local
- AWS_S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION (for s3)
- AZURE_STORAGE_CONNECTION_STRING, AZURE_CONTAINER_NAME (for azure)
- STORAGE_PREFIX: optional prefix inside bucket/container
- ADMIN_TOKEN: token for protected endpoints
- CONFIDENCE_THRESHOLD: numeric threshold for recognition confidence

## Endpoints

- GET /health
- POST /add-user/{username}  (Authorization: Bearer <ADMIN_TOKEN> recommended)
- POST /train  (Authorization required)
- POST /recognize
- GET /users
- DELETE /users/{username} (Authorization required)
- GET /models

#!/bin/bash

# Exit on error
set -e

# Check if project ID is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <GCP_PROJECT_ID>"
  exit 1
fi

# Load environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found!"
  exit 1
fi

# Set variables
PROJECT_ID=$1
IMAGE_NAME="neighbourhood-agent"
REGION="europe-west2"
IMAGE_URI="gcr.io/$PROJECT_ID/$IMAGE_NAME:latest"

echo "Building Docker image..."
docker build -t $IMAGE_URI .

echo "Pushing Docker image to Google Container Registry..."
docker push $IMAGE_URI

echo "Deploying to Cloud Run with environment variables..."
gcloud run deploy $IMAGE_NAME \
  --image $IMAGE_URI \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_PROJECT_ID=$GOOGLE_PROJECT_ID,GOOGLE_PROJECT_LOCATION=$GOOGLE_PROJECT_LOCATION,MONGO_URI="$MONGO_URI",DB_NAME=$DB_NAME,SUBSCRIPTION_ID=$SUBSCRIPTION_ID

echo "Deployment completed successfully!"

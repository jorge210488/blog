#!/bin/bash

# Variables
BUCKET_NAME="jam-blog-vue"
BUILD_DIR="dist"
DISTRIBUTION_ID="EZX73IYW7D9DX"  # ID de tu distribución de CloudFront

echo "🚀 Ejecutando build..."
npm run build

echo "🧹 Limpiando contenido anterior en S3..."
aws s3 rm s3://$BUCKET_NAME --recursive

echo "📤 Subiendo nuevo build a S3..."
aws s3 cp $BUILD_DIR s3://$BUCKET_NAME --recursive

echo "🌀 Invalidando caché de CloudFront..."
aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "/*"

echo "✅ ¡Deploy a S3 + CloudFront completado!"

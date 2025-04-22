#!/bin/bash

# Variables
BUCKET_NAME="jam-blog-vue" # cambia esto por el nombre de tu bucket
BUILD_DIR="dist"

echo "🚀 Ejecutando build..."
npm run build

echo "🧹 Limpiando contenido anterior en S3..."
aws s3 rm s3://$BUCKET_NAME --recursive

echo "📤 Subiendo nuevo build a S3..."
aws s3 cp $BUILD_DIR s3://$BUCKET_NAME --recursive

echo "✅ ¡Deploy a S3 completado!"

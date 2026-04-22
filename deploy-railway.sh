#!/bin/bash

# Railway Deployment Script for Face Emotion Detection
# This script automates the Railway deployment process

echo "🚂 Railway Deployment Script"
echo "=============================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null
then
    echo "❌ Railway CLI not found!"
    echo "📦 Installing Railway CLI..."
    npm i -g @railway/cli
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Railway CLI"
        echo "Please install manually: npm i -g @railway/cli"
        exit 1
    fi
    echo "✅ Railway CLI installed successfully"
else
    echo "✅ Railway CLI found"
fi

echo ""
echo "🔐 Logging in to Railway..."
railway login

if [ $? -ne 0 ]; then
    echo "❌ Login failed"
    exit 1
fi

echo ""
echo "✅ Login successful"
echo ""
echo "🚀 Initializing Railway project..."
railway init

if [ $? -ne 0 ]; then
    echo "❌ Initialization failed"
    exit 1
fi

echo ""
echo "✅ Project initialized"
echo ""
echo "📦 Deploying to Railway..."
railway up

if [ $? -ne 0 ]; then
    echo "❌ Deployment failed"
    exit 1
fi

echo ""
echo "✅ Deployment successful!"
echo ""
echo "🔐 Setting environment variables..."

# Generate secret key
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null)

if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  Could not generate secret key automatically"
    echo "Please set it manually:"
    echo "  railway variables set SECRET_KEY=your-secret-key"
else
    railway variables set SECRET_KEY=$SECRET_KEY
    echo "✅ SECRET_KEY set"
fi

railway variables set FLASK_ENV=production
echo "✅ FLASK_ENV set to production"

echo ""
echo "🌐 Generating domain..."
railway domain

echo ""
echo "🎉 Deployment Complete!"
echo ""
echo "📋 Next Steps:"
echo "  1. Open your app: railway open"
echo "  2. View logs: railway logs --follow"
echo "  3. Check status: railway status"
echo ""
echo "✅ Your emotion detection app is now live!"
echo "🎭 Test the webcam detection and enjoy!"
echo ""

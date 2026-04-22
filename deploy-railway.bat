@echo off
REM Railway Deployment Script for Face Emotion Detection (Windows)
REM This script automates the Railway deployment process

echo.
echo 🚂 Railway Deployment Script
echo ==============================
echo.

REM Check if Railway CLI is installed
where railway >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Railway CLI not found!
    echo 📦 Installing Railway CLI...
    call npm i -g @railway/cli
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Failed to install Railway CLI
        echo Please install manually: npm i -g @railway/cli
        exit /b 1
    )
    echo ✅ Railway CLI installed successfully
) else (
    echo ✅ Railway CLI found
)

echo.
echo 🔐 Logging in to Railway...
call railway login

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Login failed
    exit /b 1
)

echo.
echo ✅ Login successful
echo.
echo 🚀 Initializing Railway project...
call railway init

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Initialization failed
    exit /b 1
)

echo.
echo ✅ Project initialized
echo.
echo 📦 Deploying to Railway...
call railway up

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Deployment failed
    exit /b 1
)

echo.
echo ✅ Deployment successful!
echo.
echo 🔐 Setting environment variables...

REM Generate secret key
for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_hex(32))"') do set SECRET_KEY=%%i

if defined SECRET_KEY (
    call railway variables set SECRET_KEY=%SECRET_KEY%
    echo ✅ SECRET_KEY set
) else (
    echo ⚠️  Could not generate secret key automatically
    echo Please set it manually:
    echo   railway variables set SECRET_KEY=your-secret-key
)

call railway variables set FLASK_ENV=production
echo ✅ FLASK_ENV set to production

echo.
echo 🌐 Generating domain...
call railway domain

echo.
echo 🎉 Deployment Complete!
echo.
echo 📋 Next Steps:
echo   1. Open your app: railway open
echo   2. View logs: railway logs --follow
echo   3. Check status: railway status
echo.
echo ✅ Your emotion detection app is now live!
echo 🎭 Test the webcam detection and enjoy!
echo.

pause

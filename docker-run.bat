@echo off
REM Discord Meme Bot Docker Runner for Windows
REM This script helps you run the Discord bot in a Docker container

echo 🐳 Discord Meme Bot Docker Runner
echo ==================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from env_example.txt...
    if exist env_example.txt (
        copy env_example.txt .env >nul
        echo 📝 Please edit .env file with your actual credentials before running.
        echo    Required: DISCORD_TOKEN, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET
        pause
        exit /b 1
    ) else (
        echo ❌ No .env file or env_example.txt found. Please create .env file with your credentials.
        pause
        exit /b 1
    )
)

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

echo ✅ Environment check passed

echo 🚀 Starting Discord Meme Bot...
echo 📊 Use 'docker-compose logs -f' to view logs
echo 🛑 Press Ctrl+C to stop
echo.

REM Build and run the container
docker-compose up --build

echo.
echo 🛑 Bot stopped. Press any key to exit...
pause >nul 
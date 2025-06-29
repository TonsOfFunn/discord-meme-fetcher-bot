#!/bin/sh

# Alpine Linux Discord Bot Setup Script
# This script automates the installation of the Discord bot on Alpine Linux

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐧 Alpine Linux Discord Bot Setup${NC}"
echo "=================================="

# Check if running as root
if [ "$(id -u)" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Running as root. Consider creating a non-root user.${NC}"
fi

# Step 1: Update system
echo -e "${BLUE}📦 Updating Alpine packages...${NC}"
apk update
apk upgrade

# Step 2: Install essential packages
echo -e "${BLUE}📦 Installing essential packages...${NC}"
apk add git curl wget nano bash

# Step 3: Install Docker (correct Alpine package names)
echo -e "${BLUE}🐳 Installing Docker...${NC}"
apk add docker docker-cli docker-compose

# Step 4: Start and enable Docker
echo -e "${BLUE}🚀 Starting Docker service...${NC}"
rc-service docker start
rc-update add docker default

# Step 5: Create project directory
echo -e "${BLUE}📁 Setting up project directory...${NC}"
mkdir -p /opt/discord-bot
cd /opt/discord-bot

# Step 6: Clone repository (if not already present)
if [ ! -d "discord-meme-fetcher-bot" ]; then
    echo -e "${BLUE}📥 Cloning repository...${NC}"
    git clone https://github.com/TonsOfFunn/discord-meme-fetcher-bot.git
fi

cd discord-meme-fetcher-bot

# Step 7: Set up environment file
echo -e "${BLUE}⚙️  Setting up environment configuration...${NC}"
if [ ! -f ".env" ]; then
    if [ -f "env_example.txt" ]; then
        cp env_example.txt .env
        echo -e "${YELLOW}📝 Created .env file from template${NC}"
        echo -e "${YELLOW}   Please edit .env with your credentials:${NC}"
        echo -e "${YELLOW}   - DISCORD_TOKEN${NC}"
        echo -e "${YELLOW}   - REDDIT_CLIENT_ID${NC}"
        echo -e "${YELLOW}   - REDDIT_CLIENT_SECRET${NC}"
    else
        echo -e "${RED}❌ env_example.txt not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# Step 8: Create logs directory
echo -e "${BLUE}📁 Creating logs directory...${NC}"
mkdir -p logs

# Step 9: Test Docker installation
echo -e "${BLUE}🧪 Testing Docker installation...${NC}"
if docker --version > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Docker is working${NC}"
else
    echo -e "${RED}❌ Docker is not working properly${NC}"
    exit 1
fi

# Step 10: Build and run
echo -e "${BLUE}🚀 Building and starting Discord bot...${NC}"
echo -e "${YELLOW}⚠️  Make sure you've added your credentials to .env before continuing${NC}"
echo -e "${YELLOW}   Press Enter to continue or Ctrl+C to stop and edit .env${NC}"
read -r

# Build the Docker image
echo -e "${BLUE}🔨 Building Docker image...${NC}"
docker-compose build

# Start the container
echo -e "${BLUE}🚀 Starting container...${NC}"
docker-compose up -d

# Check status
echo -e "${BLUE}📊 Checking container status...${NC}"
docker-compose ps

echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo -e "${BLUE}📋 Useful commands:${NC}"
echo -e "  View logs: ${GREEN}docker-compose logs -f${NC}"
echo -e "  Stop bot:  ${GREEN}docker-compose down${NC}"
echo -e "  Restart:   ${GREEN}docker-compose restart${NC}"
echo -e "  Status:    ${GREEN}docker-compose ps${NC}"
echo ""
echo -e "${BLUE}📁 Project location: ${GREEN}/opt/discord-bot/discord-meme-fetcher-bot${NC}"
echo -e "${BLUE}📝 Edit config:      ${GREEN}nano /opt/discord-bot/discord-meme-fetcher-bot/.env${NC}" 
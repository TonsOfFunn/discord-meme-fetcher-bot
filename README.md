# 🎭 Discord Meme Fetcher Bot

A Discord bot that fetches memes from Reddit based on keywords or provides random trending memes. Built with Python using discord.py and asyncpraw (Python Reddit API Wrapper).

## ✨ Features

- **Keyword-based meme search**: Search for memes using specific keywords
- **Random meme fetching**: Get random trending memes from popular subreddits
- **Subreddit-specific search**: Search for memes in specific subreddits
- **Rich Discord embeds**: Beautiful embeds with meme information
- **Robust image detection**: Advanced image detection for various hosting platforms
- **Rate limiting protection**: Built-in delays to respect Discord rate limits
- **Cross-platform compatibility**: Works on Windows, macOS, and Linux
- **Async operations**: Non-blocking operations for better performance
- **Error handling**: Graceful error handling and user-friendly error messages
- **Input validation**: Robust input validation and whitespace handling
- **Environment variable support**: Easy configuration via environment variables
- **Comprehensive testing**: Full test suite with unit and integration tests
- **Docker support**: Easy deployment with Docker containers

## 🚀 Commands

| Command | Aliases | Description | Example |
|---------|---------|-------------|---------|
| `!meme [keyword]` | `!m` | Fetch memes by keyword or get trending memes | `!meme cat` |
| `!random [count]` | `!r` | Get random memes (default: 3, max: 10) | `!random 5` |
| `!search <keyword> [subreddit] [count]` | `!s` | Search memes in specific subreddit | `!search dog memes 3` |
| `!help` | `!h` | Show help information | `!help` |

## 📋 Prerequisites

- Python 3.8 or higher (for local development)
- Docker and Docker Compose (for containerized deployment)
- Discord Bot Token
- Reddit API Credentials

## 🛠️ Setup Instructions

### Option 1: Docker Deployment (Recommended)

#### 1. Install Docker

**Windows/macOS:**
- Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# CentOS/RHEL
sudo yum install docker docker-compose
```

#### 2. Clone the Repository

```bash
git clone https://github.com/TonsOfFunn/discord-meme-fetcher-bot.git
cd discord-meme-fetcher-bot
```

#### 3. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Copy the bot token
5. Enable the following bot permissions:
   - Send Messages
   - Embed Links
   - Attach Files
   - Use Slash Commands
   - Read Message History

#### 4. Get Reddit API Credentials

1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Fill in the details:
   - **Name**: MemeFetcherBot
   - **Type**: Script
   - **Description**: Discord bot for fetching memes
   - **About URL**: (leave blank)
   - **Redirect URI**: http://localhost:8080
4. Copy the Client ID and Client Secret

#### 5. Configure Environment Variables

1. Copy `env_example.txt` to `.env`
2. Add your credentials:

```env
# Discord Bot Configuration
DISCORD_TOKEN=your_discord_bot_token_here

# Reddit API Configuration
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
```

#### 6. Run with Docker

**Windows:**
```bash
docker-run.bat
```

**Linux/macOS:**
```bash
chmod +x docker-run.sh
./docker-run.sh
```

**Manual Docker commands:**
```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

### Option 2: Local Development

#### 1. Clone or Download the Project

```bash
git clone https://github.com/TonsOfFunn/discord-meme-fetcher-bot.git
cd discord-meme-fetcher-bot
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Copy the bot token
5. Enable the following bot permissions:
   - Send Messages
   - Embed Links
   - Attach Files
   - Use Slash Commands
   - Read Message History

#### 4. Get Reddit API Credentials

1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Fill in the details:
   - **Name**: MemeFetcherBot
   - **Type**: Script
   - **Description**: Discord bot for fetching memes
   - **About URL**: (leave blank)
   - **Redirect URI**: http://localhost:8080
4. Copy the Client ID and Client Secret

#### 5. Configure Environment Variables

1. Copy `env_example.txt` to `.env`
2. Add your credentials:

```env
# Discord Bot Configuration
DISCORD_TOKEN=your_discord_bot_token_here

# Reddit API Configuration
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
```

#### 6. Invite Bot to Your Server

1. Go to OAuth2 > URL Generator in your Discord app
2. Select "bot" scope
3. Select the permissions mentioned above
4. Copy the generated URL and open it in a browser
5. Select your server and authorize the bot

#### 7. Run the Bot

**Option 1: Using the main runner**
```bash
python run.py
```

**Option 2: Direct execution**
```bash
python discord_bot.py
```

## 🧪 Testing

The project includes a comprehensive test suite. To run tests:

**Run all tests:**
```bash
python run_tests.py
```

**Run specific test file:**
```bash
python run_tests.py test_discord_bot.py
```

**Run with pytest directly:**
```bash
pytest -v
```

**Test files included:**
- `test_config.py` - Configuration tests
- `test_reddit_client.py` - Reddit client tests
- `test_discord_bot.py` - Discord bot tests
- `test_integration.py` - Integration tests

## 🎯 Usage Examples

### Basic Commands

```bash
# Get trending memes
!meme

# Search for cat memes
!meme cat

# Get 5 random memes
!random 5

# Search for dog memes in r/memes
!search dog memes 3

# Search for programming memes in r/ProgrammerHumor
!search programming ProgrammerHumor 2
```

### Advanced Usage

- Use quotes for multi-word keywords: `!meme "funny cat"`
- Combine subreddit and count: `!search python ProgrammerHumor 5`
- Use aliases for shorter commands: `!r 3` instead of `!random 3`

## 🔧 Configuration

You can modify the bot settings in `config.py`:

- `DISCORD_PREFIX`: Change the command prefix (default: `!`)
- `MAX_MEMES_PER_REQUEST`: Maximum memes per request (default: 5)
- `DEFAULT_SUBREDDITS`: Default subreddits to search in
- `SUPPORTED_IMAGE_FORMATS`: Supported image file extensions
- `IMAGE_URL_PATTERNS`: Patterns for detecting image URLs

## 📁 Project Structure

```
discord-meme-fetcher-bot/
├── discord_bot.py          # Main Discord bot file
├── reddit_client.py        # Reddit API client
├── config.py               # Configuration settings
├── run.py                  # Main entry point script
├── run_tests.py            # Test runner script
├── requirements.txt        # Python dependencies
├── env_example.txt         # Environment variables example
├── .gitignore              # Git ignore configuration
├── README.md               # This file
├── test_config.py          # Configuration tests
├── test_reddit_client.py   # Reddit client tests
├── test_discord_bot.py     # Discord bot tests
└── test_integration.py     # Integration tests
```

## 🛡️ Safety Features

- **Rate Limiting**: Built-in delays to prevent Discord rate limits
- **Error Handling**: Graceful error handling for API failures
- **Input Validation**: Validates user input to prevent errors
- **Robust Image Detection**: Advanced detection for various image hosting platforms
- **Whitespace Handling**: Automatic trimming of user inputs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python run_tests.py`
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

### Common Issues

1. **Bot not responding**: Check if the bot token is correct and the bot has proper permissions
2. **No memes found**: Try different keywords or check if Reddit API credentials are correct
3. **Rate limit errors**: The bot has built-in rate limiting, but you can increase delays if needed
4. **Test failures**: Ensure all dependencies are installed and environment variables are set

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify your environment variables are set correctly
3. Ensure all dependencies are installed
4. Run tests to check for configuration issues
5. Check Discord and Reddit API status

## 🙏 Acknowledgments

- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- [asyncpraw](https://github.com/praw-dev/asyncpraw) - Async Python Reddit API wrapper
- Reddit community for providing amazing memes!

---

**Happy meme hunting! 🎭** 

**Made with ❤️ by TonsOfFunn**
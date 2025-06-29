import discord
from discord.ext import commands
import asyncio
import signal
import sys
from typing import Optional
from config import DISCORD_TOKEN, DISCORD_PREFIX, MAX_MEMES_PER_REQUEST, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET
from reddit_client import RedditMemeFetcher
from colorama import init, Fore as f
init(autoreset=True)

class MemeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(
            command_prefix=DISCORD_PREFIX,
            intents=intents,
            help_command=None
        )
        
        self.reddit_client = RedditMemeFetcher()
        self._shutdown_requested = False
    
    async def setup_hook(self):
        """Setup hook to load cogs and prepare the bot."""
        await self.add_cog(MemeCommands(self))
        print(f"{f.CYAN}Bot is ready! Logged in as {self.user}")
    
    async def on_ready(self):
        """Event triggered when bot is ready."""
        print(f"🎭 {f.GREEN}Meme Fetcher Bot is online!")
        if self.user:
            print(f"Bot ID: {self.user.id}")
        print(f"Prefix: {DISCORD_PREFIX}")
        print(f"{f.YELLOW}=" * 50)
    
    async def close(self):
        """Properly close the bot and all clients."""
        print("\n🔄 Shutting down bot...")
        
        # Close Reddit client
        try:
            await self.reddit_client.close()
            print("✅ Reddit client closed")
        except Exception as e:
            print(f"⚠️ Error closing Reddit client: {e}")
        
        # Close Discord client
        try:
            await super().close()
            print("✅ Discord client closed")
        except Exception as e:
            print(f"⚠️ Error closing Discord client: {e}")
        
        print(f"👋 {f.RED}Bot shutdown complete!")

class MemeCommands(commands.Cog):
    def __init__(self, bot: MemeBot):
        self.bot = bot
        self.reddit_client = bot.reddit_client
    
    @commands.command(name='meme', aliases=['m'])
    async def fetch_meme(self, ctx, *, keyword: Optional[str] = None):
        """
        Fetch memes based on a keyword or get random trending memes.
        
        Usage:
            !meme <keyword> - Search for memes with the keyword
            !meme - Get random trending memes
        """
        await ctx.typing()
        
        try:
            if keyword:
                memes = await self.reddit_client.fetch_memes_by_keyword(keyword, limit=MAX_MEMES_PER_REQUEST)
                title = f"🎭 Memes for '{keyword}'"
            else:
                memes = await self.reddit_client.get_trending_memes(limit=MAX_MEMES_PER_REQUEST)
                title = "🔥 Trending Memes"
            
            if not memes:
                embed = discord.Embed(
                    title="❌ No memes found!",
                    description="Try a different keyword or check back later.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            # Send memes one by one to avoid rate limits
            for i, meme in enumerate(memes, 1):
                embed = self.create_meme_embed(meme, title, i, len(memes))
                await ctx.send(embed=embed)
                await asyncio.sleep(1)  # Small delay between messages
                
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Error fetching memes",
                description=f"An error occurred: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
    
    @commands.command(name='random', aliases=['r'])
    async def random_memes(self, ctx, count: int = 3):
        """
        Get random memes from popular subreddits.
        
        Usage:
            !random [count] - Get random memes (default: 3, max: 10)
        """
        if count > 10:
            count = 10
        elif count < 1:
            count = 1
        
        await ctx.typing()
        
        try:
            memes = await self.reddit_client.fetch_random_memes(limit=count)
            
            if not memes:
                embed = discord.Embed(
                    title="❌ No memes found!",
                    description="Try again later.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            for i, meme in enumerate(memes, 1):
                embed = self.create_meme_embed(meme, "🎲 Random Memes", i, len(memes))
                await ctx.send(embed=embed)
                await asyncio.sleep(1)
                
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Error fetching random memes",
                description=f"An error occurred: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
    
    @commands.command(name='search', aliases=['s'])
    async def search_memes(self, ctx, keyword: str, subreddit: Optional[str] = None, count: int = 3):
        """
        Search for memes in a specific subreddit.
        
        Usage:
            !search <keyword> [subreddit] [count] - Search for memes
        """
        if count > 10:
            count = 10
        elif count < 1:
            count = 1
        
        # Clean inputs
        keyword = keyword.strip() if keyword else ""
        subreddit = subreddit.strip() if subreddit else None
        
        await ctx.typing()
        
        try:
            subreddits = [subreddit] if subreddit else None
            memes = await self.reddit_client.fetch_memes_by_keyword(keyword, subreddits, limit=count)
            
            if not memes:
                embed = discord.Embed(
                    title="❌ No memes found!",
                    description=f"No memes found for '{keyword}' in {subreddit or 'popular subreddits'}",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            
            title = f"🔍 Search results for '{keyword}'"
            if subreddit:
                title += f" in r/{subreddit}"
            
            for i, meme in enumerate(memes, 1):
                embed = self.create_meme_embed(meme, title, i, len(memes))
                await ctx.send(embed=embed)
                await asyncio.sleep(1)
                
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Error searching memes",
                description=f"An error occurred: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=error_embed)
    
    @commands.command(name='help', aliases=['h'])
    async def help_command(self, ctx):
        """Show help information about available commands."""
        embed = discord.Embed(
            title="🎭 Meme Fetcher Bot Help",
            description="A Discord bot that fetches memes from Reddit!",
            color=discord.Color.blue()
        )
        
        commands_info = [
            ("!meme [keyword]", "Fetch memes by keyword or get trending memes"),
            ("!random [count]", "Get random memes (default: 3, max: 10)"),
            ("!search <keyword> [subreddit] [count]", "Search memes in specific subreddit"),
            ("!help", "Show this help message")
        ]
        
        for cmd, desc in commands_info:
            embed.add_field(name=cmd, value=desc, inline=False)
        
        embed.add_field(
            name="📝 Examples",
            value="```\n!meme cat\n!random 5\n!search dog memes 3\n!search programming ProgrammerHumor 2```",
            inline=False
        )
        
        embed.set_footer(text="Powered by Reddit API")
        await ctx.send(embed=embed)
    
    def create_meme_embed(self, meme: dict, title: str, current: int, total: int) -> discord.Embed:
        """Create a Discord embed for a meme."""
        embed = discord.Embed(
            title=f"{title} ({current}/{total})",
            description=meme['title'],
            color=discord.Color.orange(),
            url=meme['permalink']
        )
        
        embed.set_image(url=meme['url'])
        embed.add_field(name="Subreddit", value=f"r/{meme['subreddit']}", inline=True)
        embed.add_field(name="Score", value=f"⬆️ {meme['score']}", inline=True)
        embed.add_field(name="Author", value=f"u/{meme['author']}", inline=True)
        
        # Add sorting method info if available (for random command)
        if 'sort_method' in meme:
            sort_display = meme['sort_method'].title()
            if meme['sort_method'] == 'top' and 'time_filter' in meme:
                sort_display += f" ({meme['time_filter']})"
            embed.add_field(name="Sort", value=sort_display, inline=True)
        
        # Add search method info if available (for search command)
        if 'search_method' in meme:
            embed.add_field(name="Search", value=meme['search_method'].title(), inline=True)
        
        embed.set_footer(text="Click the title to view on Reddit")
        return embed

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print(f"\n🛑 Received signal {signum}. Shutting down gracefully...")
    sys.exit(0)

async def main():
    """Main function to run the bot."""
    if not DISCORD_TOKEN:
        print("❌ Error: DISCORD_TOKEN not found in environment variables!")
        print("Please create a .env file with your Discord bot token.")
        return
    
    # Validate other required environment variables
    if not REDDIT_CLIENT_ID:
        print("❌ Error: REDDIT_CLIENT_ID not found in environment variables!")
        print("Please set REDDIT_CLIENT_ID in your .env file.")
        return
    
    if not REDDIT_CLIENT_SECRET:
        print("❌ Error: REDDIT_CLIENT_SECRET not found in environment variables!")
        print("Please set REDDIT_CLIENT_SECRET in your .env file.")
        return
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal
    
    bot = MemeBot()
    
    try:
        await bot.start(DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt received. Shutting down...")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main()) 
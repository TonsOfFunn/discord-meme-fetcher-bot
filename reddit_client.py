import asyncpraw
from typing import List, Dict, Optional
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, DEFAULT_SUBREDDITS, SUPPORTED_IMAGE_FORMATS, IMAGE_URL_PATTERNS

class RedditMemeFetcher:
    def __init__(self):
        """Initialize Reddit client for meme fetching."""
        self.reddit = asyncpraw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
    
    async def close(self):
        """Properly close the Reddit client session."""
        if hasattr(self.reddit, 'close'):
            await self.reddit.close()
    
    def is_image_post(self, post) -> bool:
        """Check if a Reddit post contains an image using robust detection."""
        url = getattr(post, 'url', None)
        if not url or not isinstance(url, str):
            return False
        
        url_lower = url.lower()
        
        # Check for standard image extensions
        if any(url_lower.endswith(ext) for ext in SUPPORTED_IMAGE_FORMATS):
            return True
        
        # Check for image hosting domains and patterns
        if any(pattern in url_lower for pattern in IMAGE_URL_PATTERNS):
            return True
        
        # Check post hint attribute (Reddit's own classification)
        post_hint = getattr(post, 'post_hint', None)
        if post_hint in ['image', 'rich:video']:
            return True
        
        # Check if it's a gallery post
        if hasattr(post, 'is_gallery') and post.is_gallery:
            return True
        
        return False
    
    def _clean_input(self, text: Optional[str]) -> Optional[str]:
        """Clean and validate input text by stripping whitespace."""
        if text is None:
            return None
        cleaned = text.strip()
        return cleaned if cleaned else None
    
    async def fetch_memes_by_keyword(self, keyword: str, subreddits: Optional[List[str]] = None, limit: int = 5) -> List[Dict]:
        """
        Fetch memes from Reddit based on a keyword.
        
        Args:
            keyword: Search keyword
            subreddits: List of subreddits to search in
            limit: Maximum number of memes to return
            
        Returns:
            List of meme dictionaries with title, url, author, subreddit, and score
        """
        # Clean inputs
        keyword = self._clean_input(keyword) or ""
        
        if subreddits is None:
            subreddits = DEFAULT_SUBREDDITS
        else:
            # Clean subreddit names and filter out None values
            cleaned_subreddits = []
            for sub in subreddits:
                cleaned = self._clean_input(sub)
                if cleaned:
                    cleaned_subreddits.append(cleaned)
            subreddits = cleaned_subreddits if cleaned_subreddits else DEFAULT_SUBREDDITS
        
        memes = []
        
        for subreddit_name in subreddits:
            try:
                subreddit = await self.reddit.subreddit(subreddit_name)
                
                # Search for posts with the keyword
                search_results = subreddit.search(keyword, sort='hot', limit=limit * 2)
                
                async for post in search_results:
                    if len(memes) >= limit:
                        break
                    
                    # Removed NSFW filter - now accepting all image posts
                    if self.is_image_post(post):
                        meme = {
                            'title': getattr(post, 'title', ''),
                            'url': getattr(post, 'url', ''),
                            'author': str(getattr(post, 'author', 'None')),
                            'subreddit': subreddit_name,
                            'score': getattr(post, 'score', 0),
                            'permalink': f"https://reddit.com{getattr(post, 'permalink', '')}"
                        }
                        memes.append(meme)
                
            except Exception as e:
                print(f"Error fetching from r/{subreddit_name}: {e}")
                continue
        
        # If we don't have enough memes from keyword search, get random hot posts
        if len(memes) < limit:
            additional_memes = await self.fetch_random_memes(limit - len(memes), subreddits)
            memes.extend(additional_memes)
        
        return memes[:limit]
    
    async def fetch_random_memes(self, limit: int = 5, subreddits: Optional[List[str]] = None) -> List[Dict]:
        """
        Fetch random hot memes from specified subreddits.
        
        Args:
            limit: Maximum number of memes to return
            subreddits: List of subreddits to fetch from
            
        Returns:
            List of meme dictionaries
        """
        if subreddits is None:
            subreddits = DEFAULT_SUBREDDITS
        else:
            # Clean subreddit names and filter out None values
            cleaned_subreddits = []
            for sub in subreddits:
                cleaned = self._clean_input(sub)
                if cleaned:
                    cleaned_subreddits.append(cleaned)
            subreddits = cleaned_subreddits if cleaned_subreddits else DEFAULT_SUBREDDITS
        
        memes = []
        
        for subreddit_name in subreddits:
            try:
                subreddit = await self.reddit.subreddit(subreddit_name)
                hot_posts = subreddit.hot(limit=limit * 2)
                
                async for post in hot_posts:
                    if len(memes) >= limit:
                        break
                    
                    # Removed NSFW filter - now accepting all image posts
                    if self.is_image_post(post):
                        meme = {
                            'title': getattr(post, 'title', ''),
                            'url': getattr(post, 'url', ''),
                            'author': str(getattr(post, 'author', 'None')),
                            'subreddit': subreddit_name,
                            'score': getattr(post, 'score', 0),
                            'permalink': f"https://reddit.com{getattr(post, 'permalink', '')}"
                        }
                        memes.append(meme)
                
            except Exception as e:
                print(f"Error fetching from r/{subreddit_name}: {e}")
                continue
        
        return memes[:limit]
    
    async def get_trending_memes(self, limit: int = 5) -> List[Dict]:
        """
        Get trending memes from popular meme subreddits.
        
        Args:
            limit: Maximum number of memes to return
            
        Returns:
            List of trending meme dictionaries
        """
        return await self.fetch_random_memes(limit, DEFAULT_SUBREDDITS)

    async def async_gen(self, items):
        for item in items:
            yield item 
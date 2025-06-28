import pytest
import os
from unittest.mock import patch

from config import (
    DISCORD_TOKEN, DISCORD_PREFIX, REDDIT_CLIENT_ID, 
    REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, MAX_MEMES_PER_REQUEST,
    DEFAULT_SUBREDDITS, SUPPORTED_IMAGE_FORMATS, IMAGE_URL_PATTERNS, get_env_var
)


class TestConfig:
    """Test suite for configuration module."""
    
    def test_discord_prefix_default(self):
        """Test that DISCORD_PREFIX has a default value."""
        assert DISCORD_PREFIX == '!'
    
    def test_max_memes_per_request_default(self):
        """Test that MAX_MEMES_PER_REQUEST has a reasonable default."""
        assert isinstance(MAX_MEMES_PER_REQUEST, int)
        assert MAX_MEMES_PER_REQUEST > 0
        assert MAX_MEMES_PER_REQUEST <= 20  # Reasonable upper limit
    
    def test_default_subreddits_structure(self):
        """Test that DEFAULT_SUBREDDITS is a list of strings."""
        assert isinstance(DEFAULT_SUBREDDITS, list)
        assert len(DEFAULT_SUBREDDITS) > 0
        
        for subreddit in DEFAULT_SUBREDDITS:
            assert isinstance(subreddit, str)
            assert len(subreddit) > 0
            # Subreddit names should not contain spaces or special chars
            assert ' ' not in subreddit
            assert subreddit.isalnum() or '_' in subreddit
    
    def test_supported_image_formats_structure(self):
        """Test that SUPPORTED_IMAGE_FORMATS contains valid extensions."""
        assert isinstance(SUPPORTED_IMAGE_FORMATS, list)
        assert len(SUPPORTED_IMAGE_FORMATS) > 0
        
        for ext in SUPPORTED_IMAGE_FORMATS:
            assert isinstance(ext, str)
            assert ext.startswith('.')
            assert len(ext) > 1  # More than just the dot
    
    def test_reddit_user_agent_format(self):
        """Test that REDDIT_USER_AGENT follows proper format."""
        assert isinstance(REDDIT_USER_AGENT, str)
        assert len(REDDIT_USER_AGENT) > 0
        assert '/' in REDDIT_USER_AGENT  # Should be in format "AppName/Version"
    
    @patch.dict(os.environ, {'DISCORD_TOKEN': 'test_discord_token'})
    def test_discord_token_from_env(self):
        """Test that DISCORD_TOKEN is loaded from environment."""
        # Re-import config to get updated values
        import importlib
        import config
        importlib.reload(config)
        
        assert config.DISCORD_TOKEN == 'test_discord_token'
    
    @patch.dict(os.environ, {'REDDIT_CLIENT_ID': 'test_client_id'})
    def test_reddit_client_id_from_env(self):
        """Test that REDDIT_CLIENT_ID is loaded from environment."""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.REDDIT_CLIENT_ID == 'test_client_id'
    
    @patch.dict(os.environ, {'REDDIT_CLIENT_SECRET': 'test_client_secret'})
    def test_reddit_client_secret_from_env(self):
        """Test that REDDIT_CLIENT_SECRET is loaded from environment."""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.REDDIT_CLIENT_SECRET == 'test_client_secret'
    
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_environment_variables(self):
        """Test behavior when environment variables are missing."""
        # Test the get_env_var function directly with a clean environment
        with patch.dict(os.environ, {}, clear=True):
            # Should be None when not set
            assert get_env_var('DISCORD_TOKEN') is None
            assert get_env_var('REDDIT_CLIENT_ID') is None
            assert get_env_var('REDDIT_CLIENT_SECRET') is None
    
    def test_default_subreddits_content(self):
        """Test that DEFAULT_SUBREDDITS contains expected subreddits."""
        expected_subreddits = ['memes', 'dankmemes', 'funny', 'me_irl', 'wholesomememes']
        
        for expected in expected_subreddits:
            assert expected in DEFAULT_SUBREDDITS
    
    def test_supported_image_formats_content(self):
        """Test that SUPPORTED_IMAGE_FORMATS contains expected formats."""
        expected_formats = ['.jpg', '.jpeg', '.png', '.gif']
        
        for expected in expected_formats:
            assert expected in SUPPORTED_IMAGE_FORMATS
    
    def test_config_values_types(self):
        """Test that all config values have correct types."""
        assert isinstance(DISCORD_PREFIX, str)
        assert isinstance(MAX_MEMES_PER_REQUEST, int)
        assert isinstance(DEFAULT_SUBREDDITS, list)
        assert isinstance(SUPPORTED_IMAGE_FORMATS, list)
        assert isinstance(REDDIT_USER_AGENT, str)
        
        # These can be None if not set in environment
        assert DISCORD_TOKEN is None or isinstance(DISCORD_TOKEN, str)
        assert REDDIT_CLIENT_ID is None or isinstance(REDDIT_CLIENT_ID, str)
        assert REDDIT_CLIENT_SECRET is None or isinstance(REDDIT_CLIENT_SECRET, str)
    
    def test_config_values_ranges(self):
        """Test that numeric config values are within reasonable ranges."""
        assert 1 <= MAX_MEMES_PER_REQUEST <= 20
        
        assert len(DEFAULT_SUBREDDITS) >= 1
        assert len(DEFAULT_SUBREDDITS) <= 10
        
        assert len(SUPPORTED_IMAGE_FORMATS) >= 1
        assert len(SUPPORTED_IMAGE_FORMATS) <= 10
    
    @patch.dict(os.environ, {
        'DISCORD_TOKEN': 'test_token_123',
        'REDDIT_CLIENT_ID': 'client_id_456',
        'REDDIT_CLIENT_SECRET': 'secret_789'
    })
    def test_all_environment_variables_set(self):
        """Test that all environment variables can be set together."""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.DISCORD_TOKEN == 'test_token_123'
        assert config.REDDIT_CLIENT_ID == 'client_id_456'
        assert config.REDDIT_CLIENT_SECRET == 'secret_789'
    
    def test_subreddit_names_valid(self):
        """Test that subreddit names follow Reddit naming conventions."""
        for subreddit in DEFAULT_SUBREDDITS:
            # Reddit subreddit names are 3-21 characters, alphanumeric + underscore
            assert 3 <= len(subreddit) <= 21
            assert subreddit.replace('_', '').isalnum()
            assert subreddit.islower()  # Reddit subreddits are lowercase
    
    def test_image_formats_valid(self):
        """Test that image formats are valid file extensions."""
        for ext in SUPPORTED_IMAGE_FORMATS:
            assert ext.startswith('.')
            assert len(ext) >= 2  # At least .x
            assert ext[1:].isalpha()  # Extension should be alphabetic
    
    def test_image_url_patterns_structure(self):
        """Test that IMAGE_URL_PATTERNS contains valid patterns."""
        assert isinstance(IMAGE_URL_PATTERNS, list)
        assert len(IMAGE_URL_PATTERNS) > 0
        
        for pattern in IMAGE_URL_PATTERNS:
            assert isinstance(pattern, str)
            assert len(pattern) > 0
    
    def test_get_env_var_function(self):
        """Test the get_env_var function with various inputs."""
        # Test with None default
        assert get_env_var('NONEXISTENT_VAR') is None
        
        # Test with custom default
        assert get_env_var('NONEXISTENT_VAR', 'default') == 'default'
        
        # Test with whitespace handling
        with patch.dict(os.environ, {'TEST_VAR': '  test_value  '}):
            assert get_env_var('TEST_VAR') == 'test_value'
        
        # Test with empty string
        with patch.dict(os.environ, {'TEST_VAR': ''}):
            assert get_env_var('TEST_VAR') is None
        
        # Test with whitespace-only string
        with patch.dict(os.environ, {'TEST_VAR': '   '}):
            assert get_env_var('TEST_VAR') is None
    
    @patch.dict(os.environ, {'DISCORD_TOKEN': ''})
    def test_empty_environment_variable(self):
        """Test behavior with empty environment variable."""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.DISCORD_TOKEN is None  # Empty string now returns None
    
    @patch.dict(os.environ, {'DISCORD_TOKEN': '   '})
    def test_whitespace_environment_variable(self):
        """Test behavior with whitespace-only environment variable."""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.DISCORD_TOKEN is None  # Whitespace-only now returns None


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
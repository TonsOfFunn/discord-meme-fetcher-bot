#!/usr/bin/env python3
"""
Test runner for Discord Meme Fetcher Bot
Runs all unit tests and integration tests with proper configuration.
"""

import sys
import os
import pytest

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    """Run all tests with proper configuration."""
    print("🧪 Running Discord Meme Fetcher Bot Tests")
    print("=" * 50)
    
    # Test files to run
    test_files = [
        "test_config.py",
        "test_reddit_client.py", 
        "test_discord_bot.py",
        "test_integration.py"
    ]
    
    # Pytest arguments (without coverage for now)
    pytest_args = [
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--color=yes",  # Colored output
        "--durations=10",  # Show 10 slowest tests
    ]
    
    # Add test files
    pytest_args.extend(test_files)
    
    try:
        # Run pytest
        result = pytest.main(pytest_args)
        
        print("\n" + "=" * 50)
        if result == 0:
            print("✅ All tests passed!")
            print("🎉 Test suite completed successfully!")
        else:
            print("❌ Some tests failed!")
            print(f"Exit code: {result}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

def run_specific_test(test_file):
    """Run a specific test file."""
    print(f"🧪 Running {test_file}")
    print("=" * 30)
    
    pytest_args = [
        "-v",
        "--tb=short",
        "--color=yes",
        test_file
    ]
    
    try:
        result = pytest.main(pytest_args)
        
        print("\n" + "=" * 30)
        if result == 0:
            print(f"✅ {test_file} passed!")
        else:
            print(f"❌ {test_file} failed!")
        
        return result
        
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return 1

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) > 1:
        # Run specific test file
        test_file = sys.argv[1]
        if not os.path.exists(test_file):
            print(f"❌ Test file {test_file} not found!")
            return 1
        return run_specific_test(test_file)
    else:
        # Run all tests
        return run_tests()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 
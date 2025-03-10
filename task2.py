import os
import tweepy
import subprocess
from dotenv import load_dotenv

# Load API credentials from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

def post_tweet(text):
    """Posts a tweet using Twitter API."""
    try:
        # Authenticate
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        # Create API object
        api = tweepy.API(auth)

        # Post tweet
        api.update_status(text)
        return "Tweet posted successfully!"
    except tweepy.TweepError as e:
        return f"Twitter API Error: {e.reason}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"

def insta_to_tweet(instagram_caption):
    """Converts an Instagram caption into a concise tweet."""
    prompt = f"Convert this Instagram caption into a short tweet under 280 characters:\n\n{instagram_caption}\n\nTweet:"
    
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.1:8b", prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        if result.returncode != 0:
            print(f"Error in Llama API call: {result.stderr}")
            return None

        response_text = result.stdout.strip()
        return response_text
    except Exception as e:
        print(f"Error in LLM processing: {str(e)}")
        return None

if __name__ == "__main__":
    instagram_caption = """The word 'Kant' means singing in our language, Malta's Eurovision 2025 act told the BBC in her first broadcast interview.

    The European Broadcasting Union ruled that Miriana Conte must change the title and the lyrics to avoid causing offence.

    The Eurovision Song Contest will be held in Basel, Switzerland, in May.

    Head to @BBCNews's bio to see the UK's Eurovision entry for 2025.

    #Eurovision #EBU #BBCNews"""

    tweet = insta_to_tweet(instagram_caption)
    if tweet:
        print("Generated Tweet:", tweet)
        response = post_tweet(tweet)
        print(response)

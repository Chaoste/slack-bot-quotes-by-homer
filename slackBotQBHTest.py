from slack import WebClient
from slackBotQBH import SlackBotQBH
import os
from dotenv import load_dotenv

load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")

# Create a slack client
slack_web_client = WebClient(token=SLACK_TOKEN)

# Get a new CoinBot
slack_bot = SlackBotQBH(f'#{SLACK_CHANNEL}')

# Get the onboarding message payload
message = slack_bot.get_message_payload()

# Post the onboarding message in Slack
slack_web_client.chat_postMessage(**message)

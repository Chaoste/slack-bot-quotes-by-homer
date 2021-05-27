import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from slackBotQBH import SlackBotQBH
from dotenv import load_dotenv

load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_EVENTS_TOKEN = os.environ.get("SLACK_EVENTS_TOKEN")
PORT = os.environ.get("PORT")

# Initialize a Flask app to host the events adapter
app = Flask(__name__)

# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(
    SLACK_EVENTS_TOKEN, "/slack/events", app)


# Initialize a Web API client
slack_web_client = WebClient(token=SLACK_TOKEN)


def pick_quote(channel):
    """Craft the SlackBotQBH, choose a quote and send the message to the channel
    """
    # Create a new SlackBotQBH
    slack_bot = SlackBotQBH(channel)

    # Get the onboarding message payload
    message = slack_bot.get_message_payload()

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**message)


@app.route('/')
def hello_world():
    return 'Hello, World!'


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    """Parse the message event, and if the activation string is in the text,
    simulate a coin flip and send the result.
    """

    # Get the event data from the payload
    event = payload.get("event", {})

    # Get the text from the event that came through
    text = event.get("text")

    channel_id = event.get("channel")

    return pick_quote(channel_id)

    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to flip a coin.
    if "quote homer" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")

        # Execute the pick_quote function and send the results of
        # flipping a coin to the channel
        return pick_quote(channel_id)


if __name__ == "__main__":
    logging.basicConfig(filename='logs/app.log', filemode='w')

    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=PORT)

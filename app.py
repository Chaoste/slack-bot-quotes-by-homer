from io import TextIOWrapper
import os
import json
import ssl
import traceback
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

logging.basicConfig(filename='logs/app.log', level=logging.DEBUG)

# Create the logging object
logger = logging.getLogger()

# Add the StreamHandler as a logging handler
logger.addHandler(logging.StreamHandler())

# Initialize a Flask app to host the events adapter
app = Flask(__name__)

# Create an events adapter and register it to an endpoint in the slack app for event injestion.
slack_events_adapter = SlackEventAdapter(
    SLACK_EVENTS_TOKEN, "/slack/events", app)


# Initialize a Web API client
slack_web_client = WebClient(token=SLACK_TOKEN)


def pick_quote(channel, f: TextIOWrapper):
    """Craft the SlackBotQBH, choose a quote and send the message to the channel
    """
    f.write("1" + "\n")
    # Create a new SlackBotQBH
    slack_bot = SlackBotQBH(channel)
    f.write("2" + "\n")

    # Get the onboarding message payload
    message = slack_bot.get_message_payload(f)
    f.write("3 " + json.dumps(message) + "\n")

    f.write("4" + "\n")
    return message


@app.route('/')
def hello_world():
    logger.debug('Hello world!')
    return 'Hello, World!'


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    f = open("logs/error.log", "a")
    try:
        """Parse the message event, and if the activation string is in the text,
        simulate a coin flip and send the result.
        """
        f.write("Slack message event received")
        f.write("\n")
        logger.debug('Slack message event received')

        # Get the event data from the payload
        event = payload.get("event", {})

        # Get the text from the event that came through
        text = event.get("text")
        f.write("- text: " + text)
        f.write("\n")

        channel_id = event.get("channel")

        f.write("- channel: " + channel_id)
        f.write("\n")

        quote = pick_quote(channel_id, f)
        f.write("- quote: " + json.dumps(quote))
        f.write("\n")

        f.write("A!?")
        f.write("\n")

        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
                getattr(ssl, '_create_unverified_context', None)):
            f.write("x")
            ssl._create_default_https_context = ssl._create_unverified_context

        f.write("B!?")
        f.write("\n")

        # Post the onboarding message in Slack
        # slack_web_client.chat_postMessage(
        #     channel=channel_id, text="Hallo Welt!")
        slack_web_client.chat_postMessage(**quote)
        f.write("C!?")
        f.write("\n")

        # return quote
    except Exception as error:
        f.write("Error when processing incoming message:")
        f.write("\n")
        f.write(repr(error))
        f.write("\n")
        f.write(traceback.format_exc())
        f.write("\n")
        # raise error
    finally:
        f.close()

    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to flip a coin.
    # if "quote homer" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        # channel_id = event.get("channel")

        # Execute the pick_quote function and send the results of
        # flipping a coin to the channel
        # return pick_quote(channel_id)


if __name__ == "__main__":
    logger.debug('Starting app...')

    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=PORT)

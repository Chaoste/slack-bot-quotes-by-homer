import os
import json
import ssl
import logging
from flask import Flask, jsonify, request
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from slackBotQBH import SlackBotQBH
from dotenv import load_dotenv

load_dotenv()
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_VERIFICATION_TOKEN = os.environ.get("SLACK_VERIFICATION_TOKEN")
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

# Src: https://moreless.medium.com/how-to-fix-python-ssl-certificate-verify-failed-97772d9dd14c
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def pick_quote(channel=None):
    """Craft the SlackBotQBH, choose a quote and return the message
    """
    # Create a new SlackBotQBH
    slack_bot = SlackBotQBH(channel)

    # Get the onboarding message payload
    message = slack_bot.get_message_payload()

    return message


def get_result(payload):
    """Craft the SlackBotQBH, evaluate the guess and return the message
    """
    # Create a new SlackBotQBH
    slack_bot = SlackBotQBH()

    # Get the onboarding message payload
    message = slack_bot.get_result_payload(payload)

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
        pick a random quote and send the result.
        """
        logger.debug('Slack message event received')

        # Get the event data from the payload
        event = payload.get("event", {})

        if event.get("bot_id") is not None:
            pass

        # Get the text from the event that came through
        text = event.get("text") or ""

        # Check and see if the activation phrase was in the text of the message.
        if "quote homer" in text.lower():
            channel_id = event.get("in_channel")
            quote = pick_quote(channel_id)

            f.write("Slack message event received")
            f.write("\n")
            f.write("- text: " + text)
            f.write("\n")
            f.write("- channel: " + channel_id)
            f.write("\n")
            f.write("- quote: " + json.dumps(quote))
            f.write("\n")

            # Post the message in Slack
            slack_web_client.chat_postMessage(**quote)

    except Exception as error:
        f.write("Error when processing incoming message:")
        f.write("\n")
        f.write(repr(error))
        f.write("\n")
    finally:
        f.close()


@app.route('/slack/command', methods=['POST'])
def slash_command():
    f = open("logs/error.log", "a")
    try:
        """Check the verification token, pick a random quote and send the result.
        """
        logger.debug('Slack slash command event received')

        if request.form.get('token') == SLACK_VERIFICATION_TOKEN:
            quote = pick_quote()

            f.write("Slack slash command event received")
            f.write("\n")
            f.write("- quote: " + json.dumps(quote))
            f.write("\n")

            return jsonify(quote)
        else:
            f.write("Verification token did not match")
            f.write("\n")

    except Exception as error:
        f.write("Error when processing incoming slash command:")
        f.write("\n")
        f.write(repr(error))
        f.write("\n")
    finally:
        f.close()

    error_response = {
        "response_type": "in_channel",
        "text": "Sorry, slash commando, that didn't work. Please try again."
    }
    return jsonify(error_response)


@app.route('/slack/interaction', methods=['POST'])
def slash_interactive_message():
    f = open("logs/error.log", "a")
    try:
        """Check the verification token, check the answer and send the result.
        """
        logger.debug('Slack interactive message event received')
        f.write(json.dumps(request.form))
        f.write("\n")

        payload: dict = json.loads(request.form.get("payload"))

        if payload.get('token') == SLACK_VERIFICATION_TOKEN:

            if payload.get('callback_id') == "quote_guess":

                f.write(str(payload.get("original_message")))
                f.write("\n")

                f.write(str(payload.get("actions")))
                f.write("\n")

                response = get_result(payload)
                return jsonify(response)
            else:
                f.write("callback_id did not match")
                f.write("\n")
        else:
            f.write("Verification token did not match")
            f.write("\n")

    except Exception as error:
        f.write("Error when processing incoming interactive message:")
        f.write("\n")
        f.write(repr(error))
        f.write("\n")
    finally:
        f.close()

    error_response = {
        "response_type": "in_channel",
        "replace_original": False,
        "text": "Sorry, slash commando, that didn't work. Please try again."
    }
    return jsonify(error_response)


if __name__ == "__main__":
    logger.debug('Starting app...')

    # Run our app on our externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=PORT)

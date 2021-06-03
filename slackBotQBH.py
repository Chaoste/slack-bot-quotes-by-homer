# import the random library to help us generate the random numbers
import sys
import random
import yaml

with open("./res/quotesHomerPoet.yaml", 'r') as stream:
    try:
        quotesHomerPoet = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit()

with open("./res/quotesHomerSimpson.yaml", 'r') as stream:
    try:
        quotesHomerSimpson = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit()


class SlackBotQBH:
    QUOTES = {
        "poet": quotesHomerPoet,
        "simpson": quotesHomerSimpson,
    }

    # Create a constant that contains the default text for the message
    QUESTION_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Who said it: Homer Simpson or the poet Homer?\n\n"
            ),
        },
    }

    # The constructor for the class. It takes the channel name as the a
    # parameter and sets it as an instance variable.
    def __init__(self, channel):
        self.channel = channel

    # Pick a random quote from the quotes array
    def _select_quote(self):
        _type = random.choice(list(self.QUOTES.keys()))
        selection = self.QUOTES[_type]["quotes"]
        picked = random.choice(selection)
        quote = f'"{picked["content"]}"'
        return {
            "blocks": [
                self.QUESTION_BLOCK,
                {"type": "section", "text": {"type": "mrkdwn", "text": quote}},
            ],
            "attachments": [
                {
                    "text": "What is your guess?",
                    "fallback": "You are unable to submit a guess",
                    "callback_id": "quote_guess",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "author",
                            "text": "Ancient Poet Homer",
                            "type": "button",
                            "value": "poet"
                        },
                        {
                            "name": "author",
                            "text": "Homer Simpson",
                            "type": "button",
                            "value": "simpson"
                        }
                    ]
                }
            ]
        }

    # Craft and return the entire message payload as a dictionary.
    def get_message_payload(self):
        content = self._select_quote()
        if self.channel is not None:
            return {
                "channel": self.channel,
                **content,
            }
        # Response to a slash command
        return {
            "response_type": "channel",
            **content,
        }

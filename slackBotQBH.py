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
    def __init__(self, channel=None):
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
                            "name": _type,
                            "text": "Ancient Poet Homer",
                            "type": "button",
                            "value": "poet"
                        },
                        {
                            "name": _type,
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
            "response_type": "in_channel",
            **content,
        }

    def _give_result(self, payload):
        guess_value = payload.get("actions")[0]["value"]
        correct_value = payload.get("actions")[0]["name"]
        # quote = payload["original_message"]["attachments"][0]["blocks"][1]["text"]["text"]

        guess_title = "Ancient Poet Homer" if guess_value == "poet" else "Homer Simpson"

        if correct_value == guess_value:
            message = f"You've chosen {guess_title} ... \n\n That's correct. Congratulations, you know a lot about literature!"
        else:
            message = f"You've chosen {guess_title} ... \n\n D'OH! That's not correct. Good luck next time!"

        return {
            "text": message
        }

        # return {
        #     "blocks": [
        #         self.QUESTION_BLOCK,
        #         {"type": "section", "text": {"type": "mrkdwn", "text": message}},
        #     ]
        # }

    # Craft and return the entire message payload as a dictionary.

    def get_result_payload(self, payload):
        content = self._give_result(payload)

        # Response to interaction
        return {
            "response_type": "ephemeral",
            "replace_original": False,
            **content,
        }

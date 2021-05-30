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
    COIN_BLOCK = {
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
    def _select_quote(self, f):
        f.write("\nGO:\n")
        _type = random.choice(list(self.QUOTES.keys()))
        f.write(self.COIN_BLOCK)
        f.write("\n")
        f.write(_type + "\n")
        f.write(self.QUOTES)
        f.write("\n")
        f.write(quotesHomerPoet)
        f.write("\n")
        f.write(self.QUOTES[_type])
        f.write("\n")
        f.write(self.QUOTES[_type]["quotes"])
        f.write("\n")
        selection = self.QUOTES[_type]["quotes"]
        f.write(selection + "\n")
        picked = random.choice(selection)
        f.write(picked + "\n")
        quote = f'"{picked["content"]}"'
        f.write(quote + "\n")
        return {"type": "section", "text": {"type": "mrkdwn", "text": quote}},

    # Craft and return the entire message payload as a dictionary.
    def get_message_payload(self, f):
        f.write("!!")
        return {
            "channel": self.channel,
            "blocks": [
                self.COIN_BLOCK,
                *self._select_quote(f),
            ],
        }

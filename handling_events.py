import os
from dotenv import load_dotenv
from slack_bolt import App
import re

load_dotenv()

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_API_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.message(":wave:")
def emoji_handler(payload, say):
    print (payload)
    say(f"Hey <@{payload['user']}>, {payload['text']}")


@app.message(re.compile("(hello|Hello)"))
def hello_handler(payload, say, context):
    say(f"Hello <@{payload['user']}>!\nHow are you?")


@app.event("reaction_added")
def reaction_added(payload, say):
    emoji = payload["reaction"]
    emoji_text = f':{emoji}:'
    say(emoji_text)


if __name__ == "__main__":
    app.start(port=5000)

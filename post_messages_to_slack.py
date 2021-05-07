import json
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_sdk.errors import SlackApiError

load_dotenv()

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_API_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

msg = {
    "blocks": [
      {
          "type": "section",
          "text": {
              "type": "mrkdwn",
              "text": "This is *first* Text"
          }
      },
        {
          "type": "section",
          "text": {
              "type": "mrkdwn",
              "text": "This is *second* text"
          }
      }
    ]
}

try:
    response = app.client.chat_postMessage(
        channel='#web-monitor', 
        blocks=msg['blocks'], 
        text='Message Received')

except SlackApiError as err:
    print(f'Message failed: {err}')

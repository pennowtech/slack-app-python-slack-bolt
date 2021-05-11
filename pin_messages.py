import os
from dotenv import load_dotenv
from slack_bolt import App

load_dotenv()

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_API_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

response = app.client.chat_postMessage(channel='#web-monitor', text="Hello!")
timestamp = response['ts']

channel_id = response['channel']
app.client.pins_add(timestamp=timestamp, channel= channel_id)
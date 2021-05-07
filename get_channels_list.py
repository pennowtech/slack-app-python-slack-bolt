import os
from dotenv import load_dotenv
from slack_bolt import App

load_dotenv()

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_API_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Fetch channels through conversation_list API
result = app.client.conversations_list(
    types="public_channel, private_channel"
)

# Print list of channels
if result.get('ok'):
    channels_list = result['channels']
    for channel in channels_list:
        print(channel['name'] + " (" + channel['id'] + ")")
else:
    print(result.get('error'))

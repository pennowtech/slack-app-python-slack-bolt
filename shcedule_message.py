import os
from dotenv import load_dotenv
from slack_bolt import App
import datetime

load_dotenv()

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_API_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

scheduled_time = datetime.datetime.now() + datetime.timedelta(seconds=120)

app.client.chat_scheduleMessage(
    channel='#web-monitor',
    post_at=scheduled_time.timestamp(),
    text="Scheduled Message: Hello"
)


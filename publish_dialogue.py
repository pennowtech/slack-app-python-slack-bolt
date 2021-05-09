import os
from dotenv import load_dotenv
from slack_bolt import App

load_dotenv()

app = App(
    token=os.environ.get("SLACK_API_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


def get_dialog_data():
    dialog_data = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Web Monitoring Configuration"
                }
            },
            {
                "type": "input",
                "block_id": "url_input_block",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "sl_input",
                            "placeholder": {
                                    "type": "plain_text",
                                    "text": "Enter URL"
                            }
                        },
                "label": {
                            "type": "plain_text",
                            "text": "URL"
                        },
                "hint": {
                            "type": "plain_text",
                            "text": "URL of website to be monitored"
                        }
            },
            {
                "type": "divider"
            },
            {
                "type": "actions",
                "block_id": "buttons_block",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                        "type": "plain_text",
                                        "text": "Submit"
                                },
                                "style": "primary",
                                "value": "submit"
                            },
                            {
                                "type": "button",
                                "text": {
                                        "type": "plain_text",
                                        "text": "Cancel"
                                },
                                "style": "danger",
                                "value": "cancel"
                            }
                        ]
            }
        ]
    }

    return dialog_data


@app.command("/webmonitor")
def webmonitor_command_handler(ack, say, payload, respond):
    ack()
    command_params = payload.get('text')

    if command_params is None:
        respond ('Nothing to do')
        return

    if command_params == 'create':
        say (blocks=get_dialog_data()['blocks'])
    else:
        respond('Invalid parameters')


if __name__ == '__main__':
    app.start(port=5000)
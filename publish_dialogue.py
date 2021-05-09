import aiohttp
import asyncio
import os
from aiohttp.client_exceptions import ClientError
from dotenv import load_dotenv
from slack_bolt import App
import dpath.util

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
                        "value": "submit",
                        "action_id": "submit_pressed"
                    },
                    {
                        "type": "button",
                        "text": {
                                "type": "plain_text",
                                "text": "Cancel"
                        },
                        "style": "danger",
                        "action_id": "cancel_pressed",
                        "value": "cancel"
                    }
                ]
            }
        ]
    }

    return dialog_data


async def async_open(url):
    web_content = None
    err_status = 'Up'
    start = asyncio.get_running_loop().time()
    try:
        async with aiohttp.request('GET',
                                   url,
                                   timeout=aiohttp.ClientTimeout(total=3)
                                   ) as resp:
            if resp.status >= 400:
                err_status = resp.reason
            web_content = await resp.text()

    except asyncio.TimeoutError as error:
        err_status = 'Timeout Error'

    except aiohttp.ClientError as error:
        err_status = 'Failed: {!r}'.format(error)

    except Exception as error:
        err_status = 'Failed'
    finally:
        time_elapsed = round((asyncio.get_running_loop().time() - start), 2)

        msg = {
            'url': url,
            'err_status': err_status if err_status else '-',
            'time': time_elapsed,
        }

        return msg


def URL_monitoring_acknowledgement(url_val):
    response = {
        "attachments": [
            {
                "color": "#f2c744",
                "blocks": [
                    {
                        "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": f"Monitoring service received for *{url_val}* :memo: \nChecking ..."
                                }
                    }
                ]
            }
        ]
    }
    return response


def URL_monitoring_response(msg):
    response = {
        "attachments": [
            {
                "color": "#754324",
                "blocks": [
                        {
                          "type": "context",
                          "elements": [
                            {
                              "type": "mrkdwn",
                              "text": f":spiral_note_pad: Monitoring Report for: {msg['url']}"
                            }
                          ]
                        },
                        {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Website Status:*\n{msg['err_status']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Time taken:*\n{msg['time']}s"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return response


@app.action("submit_pressed")
def submit_pressed_handler(ack, payload, body, respond, say):
    ack()
    url_val_obj = dpath.util.get(body, 'state/values/url_input_block/sl_input')
    if url_val_obj:
        url_val = url_val_obj.get('value')
        respond(URL_monitoring_acknowledgement(url_val))
        
        response = asyncio.run(async_open(url_val))
        say(URL_monitoring_response(response))


@app.action("cancel_pressed")
def cancel_pressed_handler(ack, say):
    ack()
    say("Cancel pressed")


@app.command("/webmonitor")
def webmonitor_command_handler(ack, say, payload, respond):
    ack()
    command_params = payload.get('text')

    if command_params is None:
        respond('Nothing to do')
        return

    if command_params == 'create':
        say(blocks=get_dialog_data()['blocks'])
    else:
        respond('Invalid parameters')


if __name__ == '__main__':
    app.start(port=5000)

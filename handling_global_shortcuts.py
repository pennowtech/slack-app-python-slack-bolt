import asyncio
import os
import aiohttp
from dotenv import load_dotenv
from dpath.segments import view
from slack_bolt import App

load_dotenv()

app = App(
    token=os.environ.get("SLACK_API_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

def job_create_view():
    view_data = {
      "type": "modal",
      "callback_id": "monitoring_job_view",
      "title": {
        "type": "plain_text",
        "text": "Website Monitoring"
      },
      "submit": {
        "type": "plain_text",
        "text": "Create"
      },
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
            "optional": True,
            "element": {
            "type": "plain_text_input",
            "action_id": "sl_input",
            "placeholder": {
              "type": "plain_text",
              "text": "Enter URL"
            },
          },
          "label": {
            "type": "plain_text",
            "text": "URL"
          },
          "hint": {
            "type": "plain_text",
            "text": "URL of website to be monitored"
          }
        }
      ]
    }

    return view_data


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



@app.view('monitoring_job_view')
def job_submitted(ack, say, respond, client, body):
    url_val = body['view']['state']['values']['url_input_block']['sl_input']['value']

    if validate_url(url_val) is None:
        ack({
          "response_action": "errors",
          "errors": {
            "url_input_block": "Please enter a valid URL"
          }
        })
    else:
        ack()
        response = asyncio.run(async_open(url_val))
        say(URL_monitoring_response(response), channel='#web-monitor')
        # respond(URL_monitoring_response(response))


# https://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python/#answer-7995979
def validate_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


@app.shortcut("webmonitor-job-cb")
def webmonitor_shortcut(ack, payload, client):
    ack()

    client.views_open(
        trigger_id=payload["trigger_id"],
        view= job_create_view()
    )

@app.shortcut("raise-website-issue-cb")
def raise_issue_shortcut(ack, payload, client):
    ack()

    client.views_open(
        trigger_id=payload["trigger_id"],
        view= job_create_view()
    )

if __name__ == '__main__':
    app.start(port=5000)

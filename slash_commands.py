import os
from dotenv import load_dotenv
from slack_bolt import App
import copy

load_dotenv()

app = App(
    token=os.environ.get("SLACK_API_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

def create_response(web_url, job_id, status, creator):
    data = {
        "text": "New Paid Time Off request from Fred Enriquez",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Web Monitoring Job",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Job ID:*\n{job_id}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*URL:*\n{web_url}"
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Created by:*\n<@{creator}>"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Status:*\n{status}"
                    }
                ]
            }
        ]
    }

    return data

def list_response(jobs_list):
    data = {
        "text": "New Paid Time Off request from Fred Enriquez",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Web Monitoring Jobs List",
                    "emoji": True
                }
            }
        ]
    }
    
    section_format = {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Job ID:*\n{job_id}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*URL:*\n{url}"
                    }
                ]
            }

    for job_id, url in enumerate(jobs_list):
        text_id = f"*Job ID:*\n{job_id}"
        text_url = f"*URL:*\n{url}"

        section_format['fields'][0]['text'] = text_id
        section_format['fields'][1]['text'] = text_url

        data['blocks'].append(copy.deepcopy(section_format))

    return data

jobs_list = []

@app.command("/webmonitor")
def webmonitor_command_handler(ack, say, payload, respond):
    ack()
    text = payload.get('text')

    if text is None:
        respond ('Nothing to do')
        return

    user = payload.get('user_name')
    command_params = tuple(text.split())

    if command_params[0] == 'create':
        url=command_params[1]
        jobs_list.append(url)
        job_id = jobs_list.index(url)
        status = "Yet to implement"
        say (create_response(url, job_id, status, user))
    elif command_params[0] == 'list':
        if jobs_list: 
            say (list_response(jobs_list))
        else:
            say ("No web monitoring jobs found.")
    else:
        respond('Invalid parameters')


if __name__ == '__main__':
    app.start(port=5000)




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


def raise_ticket_view():
    return ({
        "type": "modal",
        "callback_id": "ticket_create_view",
        "title": {
                "type": "plain_text",
                "text": "Raise a Ticket"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "blocks": [
            {
                "type": "section",
                "block_id": "ticket_info_block",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "Monitoring Report for: <http://abc.com/gc>"
                            },
                            {
                                "type": "mrkdwn",
                                "text": "*Website Status:*\nNot Found"
                            }
                        ]
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "block_id": "ticket_id_block",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": ":label: *Ticket ID: *"
                            },
                            {
                                "type": "mrkdwn",
                                "text": "1"
                            }
                        ]
            },
            {
                "type": "input",
                "block_id": "select_assignee_block",
                        "element": {
                            "type": "static_select",
                            "placeholder": {
                                    "type": "plain_text",
                                "text": "Select an assignee :woman-raising-hand:",
                                        "emoji": True
                            },
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "User 1",
                                        "emoji": True
                                    },
                                    "value": "u1"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "User 2",
                                        "emoji": True
                                    },
                                    "value": "u2"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "User 3",
                                        "emoji": True
                                    },
                                    "value": "u3"
                                }
                            ],
                            "action_id": "select_assignee_action"
                        },
                "label": {
                            "type": "plain_text",
                            "text": "Assignee",
                            "emoji": True
                        }
            },
            {
                "type": "input",
                "optional": True,
                        "block_id": "datepicker_block",
                        "element": {
                            "type": "datepicker",
                            "placeholder": {
                                    "type": "plain_text",
                                "text": "Select a planned date",
                                        "emoji": True
                            },
                            "action_id": "datepicker-action"
                        },
                "label": {
                            "type": "plain_text",
                            "text": "Date",
                            "emoji": True
                        }
            },
            {
                "type": "input",
                "block_id": "extra_detail_block",
                        "optional": True,
                        "element": {
                            "type": "plain_text_input",
                            "multiline": True,
                            "max_length": 200,
                            "action_id": "extra_detail_action"
                        },
                "label": {
                            "type": "plain_text",
                            "text": "Extra Detail",
                            "emoji": True
                        },
                "hint": {
                            "type": "plain_text",
                            "text": "Max limit is 200 characters"
                        }
            }
        ]
    })


def store_ticket(url_val, url_status, ticket_id, assignee_text, assignee_val, planned_date, extra_detail):
    return ({
        "attachments": [
            {
                "color": "#4289b9",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Ticket Raised Successfully",
                            "emoji": True
                        }
                    },
                    {
                        "type": "context",
                        "block_id": "ticket_id_block",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                    "text": ":label: *Ticket ID: *"
                            },
                            {
                                "type": "mrkdwn",
                                "text": ticket_id
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Ticket:*\n{url_val}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"{url_status}"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Planned Date:* :calendar: \n{planned_date}",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Assigne Name:*\n{assignee_text}({assignee_val})",
                            }
                        ]
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "plain_text",
                                "text": f"Extra Detail: :lower_left_fountain_pen: {extra_detail}",
                                "emoji": True
                            }
                        ]
                    }
                ]
            }
        ]
    })


def store_ticket1(url_val, url_status, ticket_id, assignee_text, assignee_val, planned_date, extra_detail):
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
                                "text": f"{url_val}, {url_status}, {ticket_id}, {assignee_text},{assignee_val}, {planned_date}, {extra_detail}"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return response


def validate_date(planned_date):
    if planned_date is None:
        return True

    import datetime
    planned_date_obj = datetime.datetime.strptime(
        planned_date, '%Y-%m-%d').date()
    cur_date = datetime.date.today()
    print(planned_date_obj)
    print(cur_date)
    print(planned_date_obj > cur_date)

    return planned_date_obj > cur_date


def process_submission_request(payload):
    values = payload['state']['values']

    # These details are retrieved from payload['blocks']
    url_val = payload['blocks'][0]['fields'][0]['text']
    url_status = payload['blocks'][0]['fields'][1]['text']
    ticket_id = payload['blocks'][2]['elements'][1]['text']

    # These details are retrieved from payload['state']['values]
    assignee_val = values['select_assignee_block']['select_assignee_action']['selected_option']['value']
    assignee_text = values['select_assignee_block']['select_assignee_action']['selected_option']['text']['text']
    planned_date = values['datepicker_block']['datepicker-action']['selected_date']
    extra_detail = values['extra_detail_block']['extra_detail_action']['value']

    return store_ticket(url_val, url_status, ticket_id, assignee_text, assignee_val, planned_date, extra_detail)


@app.view("ticket_create_view")
def ticket_submitted(ack, payload, body, say):
    planned_date = payload['state']['values']['datepicker_block']['datepicker-action']['selected_date']
    if validate_date(planned_date) is False:
        ack({
            "response_action": "errors",
            "errors": {
                "datepicker_block": "Planned date can't be in past"
            }
        })
    else:
        ack()

        say(process_submission_request(payload), channel='#web-monitor')


@app.shortcut("raise-website-issue-cb")
def raise_issue_shortcut(ack, payload, client):
    ack()

    client.views_open(
        trigger_id=payload["trigger_id"],
        view=raise_ticket_view()
    )


if __name__ == '__main__':
    app.start(port=5000)

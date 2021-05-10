import os
from dotenv import load_dotenv
from slack_bolt import App

load_dotenv()

app = App(
    token=os.environ.get("SLACK_API_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


def employee_view():
    return ({
	"type": "modal",
	"callback_id": "employee_view",
	"title": {
		"type": "plain_text",
		"text": "Employee information"
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit"
	},
	"blocks": [
		{
			"type": "input",
			"block_id": "name_input_block",
			"element": {
				"type": "plain_text_input",
				"action_id": "name_input",
				"placeholder": {
					"type": "plain_text",
					"text": "Enter employee's name"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Name"
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action",
				"placeholder": {
					"type": "plain_text",
					"text": "Enter employee's department"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Department",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "If you want to select from department list:"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Click Me",
					"emoji": True
				},
				"value": "click_me_123",
				"action_id": "button-action"
			}
		}
	]
})

def employee_view_with_department_list(employee_name):
    return ({
	"type": "modal",
	"callback_id": "employee_view_with_department_list",
	"title": {
		"type": "plain_text",
		"text": "Employee information"
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit"
	},
	"blocks": [
		{
			"type": "input",
			"block_id": "name_input_block",
			"element": {
				"type": "plain_text_input",
				"action_id": "name_input",
				"placeholder": {
					"type": "plain_text",
					"text": employee_name if employee_name else "Enter employee's name"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Name"
			}
		},
		{
			"type": "input",
			"block_id": "department_select_block",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Electrical",
							"emoji": True
						},
						"value": "electrical"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Management",
							"emoji": True
						},
						"value": "management"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Mechanical",
							"emoji": True
						},
						"value": "mechanical"
					}
				],
				"action_id": "department_select_action"
			},
			"label": {
				"type": "plain_text",
				"text": "Department",
				"emoji": True
			}
		}
	]
})

@app.view('employee_view_with_department_list')
def employee_view_submission(ack, say, respond, client, body):
    ack()
    employee_name = body['view']['state']['values']['name_input_block']['name_input']['value']
    employee_deptt = body['view']['state']['values']['department_select_block']['department_select_action']['selected_option']['value']

    text=(f"Employee name: {employee_name}. "
          f"Employee department: {employee_deptt}")
    print(text)



@app.action("button-action")
def update_employee_view(ack, body, client, payload):
    ack()
    print(payload)
    print('----')
    print(body)
    employee_name = body['view']['state']['values']['name_input_block']['name_input']['value']
    view_info = employee_view_with_department_list(employee_name)

    # client.views_push(
    #     trigger_id=body["trigger_id"],
    #     view=view_info
    # )


@app.command("/employee")
def employee_command_handler(ack, payload, client):
    ack()

    client.views_open(
        trigger_id=payload["trigger_id"],
        view=employee_view()
    )


if __name__ == '__main__':
    app.start(port=5000)

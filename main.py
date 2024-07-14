import datetime
import sys

from todoist_api_python.api import TodoistAPI
from tqdm import tqdm

import utils
from notion_helper import get_notion_header, is_active_in_notion, post_status_to_notion
from todoist_helper import build_task_list, update_task_due_date, get_todoist_header

# set to true for IDE execution
local_execution = False

if local_execution:
    json = utils.read_json('constants_todoist_reschedule_overdue.json')
else:
    json = utils.read_json('/home/ubuntu/todoist-reschedule-overdue/constants_todoist_reschedule_overdue.json')

# retrieve values from json file
todoist_api_token = json['todoist_api_token']
todoist_api_version = json['todoist_api_version']
notion_api_token = json['notion_api_token']
notion_api_version = json['notion_api_version']
integration_page_id = json['integration_page_id']

# set headers
todoist_header = get_todoist_header(todoist_api_token)
notion_header = get_notion_header(notion_api_token, notion_api_version)

try:
    # check if integration is active in Notion
    if not is_active_in_notion(notion_header, integration_page_id):
        sys.exit('Inactive in Notion. Exiting...')

    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(days=1))

    api = TodoistAPI(todoist_api_token)

    # retrieve all tasks from Todoist
    task_list = build_task_list(todoist_header, todoist_api_version)

    # identify overdue tasks
    overdue_tasks = []
    for task in task_list:
        if task['date'] == str(yesterday):
            overdue_tasks.append(task)
    
    # reschedule overdue tasks
    rescheduled_tasks = []
    for task in tqdm(overdue_tasks, disable=not local_execution):
        update_task_due_date(todoist_header, todoist_api_version, today, task['id'], task['string'], task['is_recurring'])
        rescheduled_tasks.append(task)

    print('Rescheduled ' + str(len(rescheduled_tasks)) + ' overdue task(s)')

    # log result in Notion
    post_status_to_notion(notion_header, integration_page_id, True)
except Exception as e:
    print(e)
    post_status_to_notion(notion_header, integration_page_id, False)

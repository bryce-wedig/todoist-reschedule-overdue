import requests
from pprint import pprint


def get_all_tasks(auth_todoist, todoist_api_version):
    return requests.get("https://api.todoist.com/api/" + todoist_api_version + "/tasks", headers=auth_todoist)


def update_task(auth_todoist, todoist_api_version, task_id, body):
    return requests.post("https://api.todoist.com/api/" + todoist_api_version + "/tasks/" + task_id,
                         headers=auth_todoist,
                         data=body)

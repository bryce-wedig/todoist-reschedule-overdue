import requests
from pprint import pprint


def get_all_tasks(auth_todoist, todoist_api_version):
    url = "https://api.todoist.com/api/" + todoist_api_version + "/tasks"
    all_tasks = []
    cursor = None

    while True:
        params = {}
        if cursor:
            params['cursor'] = cursor

        response = requests.get(url, headers=auth_todoist, params=params)
        response.raise_for_status()
        data = response.json()

        all_tasks.extend(data['results'])

        cursor = data.get('next_cursor')
        if not cursor:
            break

    return all_tasks


def update_task(auth_todoist, todoist_api_version, task_id, body):
    return requests.post("https://api.todoist.com/api/" + todoist_api_version + "/tasks/" + task_id,
                         headers=auth_todoist,
                         data=body)

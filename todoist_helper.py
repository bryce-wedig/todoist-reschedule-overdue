import json

import todoist_client


def build_task_list(auth_todoist, todoist_api_version):
    # get all tasks
    all_tasks_response = todoist_client.get_all_tasks(auth_todoist, todoist_api_version)
    all_tasks_dict = json.loads(all_tasks_response.text)

    task_list = []

    for each in list(all_tasks_dict):
        task = {'id': each['id']}
        due_dict = each.get('due')

        if due_dict is not None:
            task['is_recurring'] = due_dict['is_recurring']
            task['string'] = due_dict['string']
            task['date'] = due_dict['date']
        else:
            task['recurring'] = None
            task['string'] = None
            task['date'] = None

        # get additional fields for export
        task['project_id'] = each['project_id']
        task['section_id'] = each['section_id']
        task['content'] = each['content']
        task['created_at'] = each['created_at']

        task_list.append(task)

    return task_list


def update_task_due_date(auth_todoist, todoist_api_version, today, task_id, due_string, recurring):
    auth_todoist.update({"Content-Type": "application/json"})

    if recurring is True:
        body = json.dumps({
            "due_date": str(today),
            "due_string": due_string
        })

        # TODO try catch block
        response = todoist_client.update_task(auth_todoist, todoist_api_version, task_id, body)
        # print(response.text)

    else:
        body = json.dumps({
            "due_date": str(today)
        })

        response = todoist_client.update_task(auth_todoist, todoist_api_version, task_id, body)
        # print(response.text)


def get_recurring_tasks(task_list, yesterday):
    recurring_tasks = []

    for task in task_list:
        if task['is_recurring'] and task['date'] == str(yesterday):
            recurring_tasks.append(task)

    return recurring_tasks


def get_onetime_tasks(task_list, yesterday):
    onetime_tasks = []

    for task in task_list:
        if not task['is_recurring'] and task['date'] == str(yesterday):
            onetime_tasks.append(task)

    return onetime_tasks


def get_todoist_header(todoist_api_token):
    return {"Authorization": "Bearer " + todoist_api_token}

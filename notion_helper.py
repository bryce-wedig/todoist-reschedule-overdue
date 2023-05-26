import datetime
import json

import notion_client


def is_active_in_notion(notion_header, integration_page_id):
    query_active = notion_client.get_property_item(notion_header, integration_page_id, "ia%3Dl")

    return json.loads(query_active.text)["checkbox"]


def post_status_to_notion(notion_header, integration_page_id, is_success):
    if is_success:
        message = "Ran successfully at " + str(datetime.datetime.today())
    else:
        message = "Failed to run at " + str(datetime.datetime.today())

    return notion_client.set_status(notion_header, integration_page_id, message)


def get_notion_header(notion_api_token, notion_api_version):
    return {
        "Authorization": "Bearer " + notion_api_token,
        "Content-Type": "application/json",
        "Notion-Version": notion_api_version
    }

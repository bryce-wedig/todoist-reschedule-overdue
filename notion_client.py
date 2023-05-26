import json

import requests


def get_property_item(notion_header, integration_page_id, item_id):
    return requests.get(
        "https://api.notion.com/v1/pages/" + integration_page_id + "/properties/" + item_id,
        headers=notion_header
    )


def set_status(notion_header, integration_page_id, message):
    return requests.patch(
        "https://api.notion.com/v1/pages/" + integration_page_id,
        headers=notion_header,
        data=json.dumps({
            "properties": {
                "Status": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": message
                            },
                            "plain_text": message
                        }
                    ]
                }
            }
        })
    )

import json
from typing import Any
from urllib.parse import quote

import requests


class ConfluenceSDK:
    def __init__(self, project: str, username: str, password: str) -> None:
        self.project = project
        self.auth = (username, password)

        self.headers = {
            "Content-Type": "application/json",
        }
        self.baseurl = f"https://{self.project}.atlassian.net"

    def fetch_all_spaces(self, limit: int = 25) -> list[dict[str, Any]]:
        url = f"{self.baseurl}/wiki/rest/api/space?limit={limit}"

        response = requests.request(
            method="GET",
            url=url,
            auth=self.auth,
            headers=self.headers,
        )

        spaces = json.loads(response.content)["results"]

        return spaces

    def get_space_key_by_space_name(self, space_name: str) -> str | None:
        space_name = quote(space_name)

        all_spaces = self.fetch_all_spaces(limit=1000)

        space_name_dict = dict(
            zip([i["name"] for i in all_spaces], [i["key"] for i in all_spaces])
        )

        space_key = space_name_dict.get(space_name, None)
        return space_key

    def fetch_space_by_name(self, space_name: str) -> requests.Response:
        space_name = quote(space_name)
        space_key = self.get_space_key_by_space_name(space_name)
        url = f"{self.baseurl}/wiki/rest/api/space?spaceKey={space_key}"

        response = requests.request(
            method="GET",
            url=url,
            auth=self.auth,
            headers=self.headers,
        )

        space = json.loads(response.content)["results"]
        return space

    def fetch_space_by_key(self, space_key: str) -> requests.Response:
        space_key = quote(space_key)
        url = f"{self.baseurl}/wiki/rest/api/space?spaceKey={space_key}"

        response = requests.request(
            method="GET",
            url=url,
            auth=self.auth,
            headers=self.headers,
        )

        space = json.loads(response.content)["results"]
        return space

    def fetch_pageID_by_name(self, space_name: str, page_title: str) -> int:
        space_name = quote(space_name)
        space_key = self.get_space_key_by_space_name(space_name)
        page_title = quote(page_title)
        url = (
            f"{self.baseurl}/wiki/rest/api/content?"
            f"title={page_title}&spaceKey={space_key}"
        )

        response = requests.request(
            method="GET",
            url=url,
            auth=self.auth,
            headers=self.headers,
        )
        pageID = json.loads(response.text)["results"][0]["id"]
        return int(pageID)

    def push_new_page(
        self,
        space_name: str,
        page_title: str,
        page_content: str,
        parent_page_id: int | None = None,
    ) -> None:
        space_key = self.get_space_key_by_space_name(space_name)
        data = {
            "type": "page",
            "title": page_title,
            "space": {"key": space_key},
            "body": {"storage": {"value": page_content, "representation": "storage"}},
        }

        if parent_page_id is not None:
            data["ancestors"] = [{"id": parent_page_id}]

        response = requests.request(
            method="POST",
            url=f"{self.baseurl}/wiki/rest/api/content",
            auth=self.auth,
            headers=self.headers,
            data=json.dumps((data)),
        )

        if response.status_code <= 204:
            print(f"Page published to the server: {page_title}")
        else:
            print(
                f"Error Code: {response.status_code} -> "
                f"{json.loads(response.text)['message']}"
            )

    def get_children_page_ids(
        self, space_name: str, page_title: str, limit: int = 25
    ) -> list[int]:
        parent_page_id = self.fetch_pageID_by_name(
            space_name=space_name, page_title=page_title
        )

        url = (
            f"{self.baseurl}/wiki/rest/api/content/{parent_page_id}/child/page?"
            f"limit={limit}"
        )

        response = requests.request(
            method="GET",
            url=url,
            auth=self.auth,
            headers=self.headers,
        )

        response_dict = json.loads(response.text)
        children_page_ids = [obj["id"] for obj in response_dict["results"]]

        return children_page_ids

    def delete_page_by_id(self, page_id: int) -> None:
        url = f"{self.baseurl}/wiki/rest/api/content/{page_id}"

        response = requests.request(
            method="DELETE",
            url=url,
            auth=self.auth,
            headers=self.headers,
        )

        if response.status_code <= 204:
            print(f"Page id: {page_id} has been deleted!")
        else:
            print(
                f"Error Code: {response.status_code} -> "
                f"{json.loads(response.text)['message']}"
            )

    def delete_children_pages(
        self, space_name: str, parent_page_name: str, limit: int = 100
    ) -> None:
        pages_to_delete = self.get_children_page_ids(
            space_name, parent_page_name, limit=limit
        )
        while len(pages_to_delete) > 0:
            # Children page ids is limited by given parameters, so adding '+' if necessary
            if len(pages_to_delete) > limit:
                print(f"Total pages to delete: {len(pages_to_delete)}+")
            else:
                print(f"Total pages to delete: {len(pages_to_delete)}")

            for i in pages_to_delete:
                self.delete_page_by_id(i)

            pages_to_delete = self.get_children_page_ids(
                space_name, parent_page_name, limit
            )
        else:
            print(f"No pages found to delete under: {parent_page_name}")

    @staticmethod
    def pretty_text(response: requests.Response) -> None:
        print(
            json.dumps(
                json.loads(response.text),
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
            )
        )

    def __str__(self) -> str:
        return f"ConfluenceSDK @ {self.project}"

    def __repr__(self) -> str:
        return f"ConfluenceSDK @ {self.project}"

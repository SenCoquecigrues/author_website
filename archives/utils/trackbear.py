import aiohttp
import logging

from django.conf import settings


class TrackbearConnector:
    BASE_URL = 'https://trackbear.app/api/v1'
    USER_AGENT = settings.TRACKBEAR_AGENT

    async def get_author_projects(author_profile):
        bear_headers={
            "Authorization": f"Bearer {author_profile.trackbear_api_key}",
            "User-Agent": TrackbearConnector.USER_AGENT
        }
        async with aiohttp.ClientSession(headers=bear_headers) as session:
            async with session.get(f"{TrackbearConnector.BASE_URL}/project") as response:
                json_body = await response.json()

                if not json_body["success"]:
                    logging.error(f"Error fetching Trackbear data for {author_profile.nickname} : {json_body["error"]["code"]}")
                    return json_body["error"]

                if json_body["success"]:
                    return TrackbearConnector.format_author_projects(json_body["data"])

    def format_author_projects(projects_list: list) -> list:
        results = []

        for project in projects_list:
            if project["displayOnProfile"]:
                results.append(TrackbearConnector.format_project(project))
            else:
                print(f'{project["title"]} : {project["displayOnProfile"]}')

        return results

    def format_project(project: dict) -> dict:
        return {
            "title": project["title"],
            "description": project["description"],
            "phase": project["phase"],
            "total_words": project["totals"]["words"],
            "total_time": project["totals"]["time"],
            "total_chapters": project["totals"]["chapters"],
            "total_scenes": project["totals"]["scenes"],
        }

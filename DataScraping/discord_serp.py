import requests
import os
import json


def get_servers(keyword: str):
    url = "https://search.discordservers.com/?term=" + keyword + "&size=30&from=0"
    res = requests.get(url).json()
    servers = []
    for result in res.get("results"):
        for key in result.keys():
            print(key)
        servers.append(
            {
                "title": result.get("name"),
                "members": result.get("members"),
                "premium": result.get("premium"),
                "description": result.get("description"),
                "customInvite": result.get("customInvite"),
                "categories": result.get("categories"),
                "iconUrl": result.get("iconUrl"),
            }
        )
    return servers
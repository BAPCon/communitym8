import requests
import json

twitch_graphql = "https://gql.twitch.tv/gql"
twitch_headers = None
twitch_payload = None

serp_api_key = None


def search(query):
    params = {
        "api_key": serp_api_key,
        "q": query + " site:twitch.tv -directory /home",
        "location": "United States",
        "num": "10",
    }
    api_result = requests.get("https://api.scaleserp.com/search", params).json()
    users = []
    for result in api_result.get("organic_results"):
        screen_name = result.get("title").split(" - ")[0]
        user_name = result.get("link").split(".tv/")[1]
        if user_name.count("/") > 0:
            user_name = user_name.split("/")[0]
        users.append(
            {
                "screen_name": screen_name,
                "user_name": user_name,
                "description": result.get("snippet"),
                "link": "https://twitch.tv/" + screen_name,
            }
        )
        if users[-1].get("screen_name") == "Twitch":
            users[-1]["screen_name"] = users[-1].get("user_name")
            users[-1]["link"] = "https://twitch.tv/" + users[-1].get("user_name")

    for i in range(0, len(users)):
        twitch_res = get_user(users[i].get("screen_name"))
        users[i]["thumbnail"] = twitch_res[0]
        users[i]["followers"] = twitch_res[1]

    return users


def get_user(username):

    res = requests.request(
        "POST", twitch_graphql, headers=twitch_headers, data=twitch_payload
    ).json()
    path = [
        "data",
        "user",
        "videoShelves",
        "edges",
        "node",
        "items",
        "owner",
        "profileImageURL",
    ]

    thumbnail = None
    followers = None

    for node in res:
        response = node
        for path_node in path:
            if response == None:
                break

            if isinstance(response.get(path_node), list):
                response = response.get(path_node)[0]
            else:
                if response.get("followers") != None:
                    followers = response.get("followers").get("totalCount")
                response = response.get(path_node)

        if response != None:
            if response.count("dn.jtvnw.net/jtv_user_pictures/") > 0:
                thumbnail = response.replace("50x50", "300x300")

    return [thumbnail, followers]
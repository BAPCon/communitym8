import requests
import os
import json


serp_api_key = None
consumer_key = None
consumer_sec = None
bearer_token = None


def get_user(user_id):
    url = "https://api.twitter.com/1.1/users/show.json?user_id=" + user_id
    res = requests.get(url, headers={"authorization": "Bearer " + bearer_token})
    return res.json()


def get_user_from_name(user_id):
    url = "https://api.twitter.com/1.1/users/show.json?screen_name=" + user_id
    res = requests.get(url, headers={"authorization": "Bearer " + bearer_token}).json()
    if res.get("errors") != None:
        return None
    urls = []
    try:
        for url in res.get("entities").get("url").get("urls"):
            urls.append({"short_url": url.get("url"), "link": url.get("expanded_url")})
    except:
        pass
    try:
        for url in res.get("entities").get("description").get("urls"):
            urls.append({"short_url": url.get("url"), "link": url.get("expanded_url")})
    except:
        pass

    user = {
        "id": res.get("id"),
        "name": res.get("name"),
        "description": res.get("description"),
        "url": res.get("url"),
        "links": urls,
        "followers_count": res.get("followers_count"),
        "friends_count": res.get("friends_count"),
        "verified": res.get("verified"),
        "profile_background_image_url": res.get("profile_background_image_url"),
        "profile_background_image_url_https": res.get(
            "profile_background_image_url_https"
        ),
        "profile_image_url": res.get("profile_image_url"),
        "profile_image_url_https": res.get("profile_image_url_https"),
        "profile_banner_url": res.get("profile_banner_url"),
    }
    return user


def serp_communities(query):
    params = {
        "api_key": serp_api_key,
        "q": query + " communities twitter site:twitter.com",
        "gl": "us",
        "hl": "en",
    }

    api_result = requests.get("https://api.scaleserp.com/search", params)
    users = []
    for result in api_result.json().get("organic_results"):
        if result.get("link").count("twitter.com") > 0:
            if result.get("title").count("(") > 0:
                users.append(
                    {
                        "username": result.get("title").split("(")[1].split(")")[0],
                        "link": result.get("link"),
                        "description": result.get("snippet"),
                    }
                )
            else:
                users.append(
                    {
                        "username": result.get("link").split("/")[-1],
                        "link": result.get("link"),
                        "description": result.get("snippet"),
                    }
                )

    return users


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def search_twitter(query):
    params = {"query": query, "tweet.fields": "author_id"}
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/recent",
        auth=bearer_oauth,
        params=params,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    res = json.dumps(response.json()).encode("ascii", "ignore")
    res = str(res)[2:-1].replace("\\", "")
    res = json.loads(res)
    print(res)
    deduped_users = []
    for tweet in res.get("data"):
        if deduped_users.count(tweet.get("author_id")) == 0:
            deduped_users.append(tweet.get("author_id"))

    return deduped_users


def search(query: str, serp_result=None):
    if serp_result == None:
        serp_result = serp_communities(query)
        accounts = []
        left_over = None
        left_over = serp_result[3:]

    for user in serp_result:
        twitter_data = get_user_from_name(user.get("username").replace("@", ""))
        for key in user.keys():
            twitter_data[key] = user.get(key)
        accounts.append(twitter_data)
    left_over = serp_result[12:]

    return {"accounts": accounts, "left_over": left_over}
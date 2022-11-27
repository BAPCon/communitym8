import os
import googleapiclient.discovery
import random

api_key = None
max_results = 35


def search(query: str):
    res = youtube_video_search(query)

    res_info = res.get("pageInfo")
    res_info["nextPage"] = res.get("nextPageToken")

    video_data = set_results(res.get("items"))

    res = youtube_channel_info(video_data.get("channels"))

    channel_data = set_channel_results(res.get("items"))
    return {"channels": channel_data, "videos": video_data}


def set_results(results: list):
    deduped_channels = []
    videos = []
    id_counts = []
    for item in results:
        snippet = item.get("snippet")
        try:
            cid = snippet.get("channelId")
            if deduped_channels.count(cid) == 0:
                deduped_channels.append(cid)
                id_counts.append(1)
            else:
                id_counts[deduped_channels.index(cid)] += 1
        except:
            pass
        tns = snippet.get("thumbnails")
        thumbnail = (
            tns.get("high")
            if tns.get("high") != None
            else tns.get("medium")
            if tns.get("medium") != None
            else tns.get("default")
        )
        videos.append(
            {
                "id": item.get("id").get("videoId"),
                "etag": item.get("etag"),
                "publish_date": snippet.get("publishedAt"),
                "channel_id": cid,
                "title": snippet.get("title"),
                "partial_description": snippet.get("description"),
                "thumbnail": thumbnail,
            }
        )

    channel_sorting = []
    for channel in deduped_channels:
        channel_sorting.append(
            {
                "id": channel,
                "position": (
                    id_counts[deduped_channels.index(channel)]
                    + (len(deduped_channels) - deduped_channels.index(channel))
                )
                / 2,
            }
        )
    channel_sorting = sorted(channel_sorting, key=lambda d: d["position"], reverse=True)

    return {"videos": videos, "channels": channel_sorting}


def set_channel_results(channels: list):
    formatted_results = []
    for result in channels:
        snippet = result.get("snippet")
        tns = snippet.get("thumbnails")
        thumbnail = (
            tns.get("high")
            if tns.get("high") != None
            else tns.get("medium")
            if tns.get("medium") != None
            else tns.get("default")
        )
        formatted_results.append(
            {
                "id": result.get("id"),
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "customUrl": snippet.get("customUrl"),
                "views": result.get("statistics").get("viewCount"),
                "subscribers": result.get("statistics").get("subscriberCount"),
                "thumbnail": thumbnail,
            }
        )

    return formatted_results


def youtube_video_search(query: str):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = api_key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )

    request = youtube.search().list(
        part="snippet",
        maxResults=max_results,
        q=query + " " + random.choice(["explained", "commentary", "debate"]),
    )
    return request.execute()


def youtube_channel_info(channel_param: list):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = api_key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )
    channel_ids = []
    for channel in channel_param:
        channel_ids.append(channel.get("id"))

    request = youtube.channels().list(
        part="snippet,contentDetails,contentOwnerDetails,statistics,status",
        id=",".join(channel_ids),
    )
    return request.execute()
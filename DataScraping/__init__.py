from DataScraping import discord_serp as discord, twitter, youtube, twitch


def set_credentials(youtube_key: None, twitter_token: None):
    if youtube_key != None:
        youtube.api_key = youtube_key
    if twitter_token != None:
        twitter.bearer_token = twitter_token


def search(query):
    discord_servers = discord.get_servers(query)
    youtube_channels = youtube.search(query)
    twitter_users = twitter.search(query)
    twitch_users = twitch.search(query)

    return {
        "youtube_data": youtube_channels,
        "discord_servers": discord_servers,
        "twitter_users": twitter_users,
        "twitch_users": twitch_users,
    }

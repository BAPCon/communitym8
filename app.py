import DataScraping as scraper
import json
import random
from flask import Flask, request


scraper.set_credentials("youtube_key", "twitter_token")
app = Flask(__name__)


@app.route("/images/<file_name>")
def image(file_name):
    return open(file_name, "rb").read()


@app.route("/")
def index():
    return open("index.html", "r").read()


@app.route("/search")
def search():
    card_html = open("card.html", "r").read()
    card_rows = open("cardresult.html", "r").read()
    query = request.args.get("query", "")
    random_query = [
        "science",
        "education",
        "unboxing",
        "reviews",
        "how to",
        "talkshow",
        "gaming",
        "talent",
        "music",
        "news",
        "politics",
        "philosophy",
        "culture",
        "sports",
        "art",
        "painting",
        "drawing",
        "commentary",
    ]
    if query == "":
        query = random_query[random.randint(0, len(random_query) - 1)]
    try:
        search_data = json.loads(open("datastore/" + query + ".json", "r").read())
    except:
        search_data = scraper.search(
            query
        )  # json.loads(open('test_data_new.json',"r").read())
        f = open("datastore/" + query + ".json", "w")
        f.write(json.dumps(search_data))
        f.close()
    rows = []
    column_count = 3
    accountsbr = []
    item_count = 0
    pls = ["discord", "twitter", "youtube", "twitch"]
    for i in range(0, 5):
        cards = []
        for x in range(0, column_count):

            tmpe = card_html.replace(
                "WIDTH_DIMENSION", str(card_result_dimensions(column_count)[0])
            ).replace("MARGIN_DIMENSION", str(card_result_dimensions(column_count)[1]))
            platform = pls[random.randint(0, len(pls) - 1)]
            try:
                if (
                    platform == "discord"
                    and len(search_data.get("discord_servers")) > 1
                ):
                    tar = search_data.get("discord_servers")[
                        random.randint(0, len(search_data.get("discord_servers")) - 1)
                    ]
                    br = 0
                    while accountsbr.count(tar) > 0 and br < 15:
                        tar = search_data.get("discord_servers")[
                            random.randint(
                                0, len(search_data.get("discord_servers")) - 1
                            )
                        ]
                        br += 1
                    if br >= 13:
                        pls.remove(platform)
                        cards.append(get_video_to_add(tmpe, search_data))
                        continue
                    accountsbr.append(tar)
                    tmpe = tmpe.replace(
                        "USER_TITLE",
                        str(
                            tar.get("title")[
                                : min(len(tar.get("title")), len("PepoBets | CSGO"))
                            ].encode("ascii", "ignore")
                        )[2:-1],
                    )
                    tmpe = tmpe.replace("images/PLATFORM_NAME.png", tar.get("iconUrl"))
                    tmpe = tmpe.replace("PLATFORM_NAME", "Discord")
                    tmpe = tmpe.replace(
                        "TARGET_URL",
                        "https://discord.com/guilds/"
                        + tar.get("iconUrl").split("icons/")[1].split("/")[0],
                    )
                    body_fill = (
                        tar.get("description")
                        .replace("/", " / ")
                        .replace(",", " , ")
                        .replace("  ", " ")
                        .replace(" ,", ",")
                    )
                    cut_off_length = len(
                        "The Scrimmage official discord server: Features: Sports / Sports betting chats Bots that bring in schedules, odds, trends, and both team and player stats. Live New"
                    )
                    if len(body_fill) > cut_off_length:
                        body_fill = body_fill[:cut_off_length] + "..."
                    tmpe = tmpe.replace("BODY_FILL", body_fill)
                    sbcs = int(tar.get("members"))
                    if sbcs >= 1000000:
                        sbcs = str((sbcs - (sbcs % 100000)) / 1000000) + "m"
                    else:
                        if sbcs >= 100000:
                            sbcs = str((sbcs - (sbcs % 1000)) / 100000)
                            if sbcs.count(".") > 0:
                                if len(sbcs.split(".")[1]) > 1:
                                    sbcs = (
                                        sbcs.split(".")[0] + "." + sbcs.split(".")[1][0]
                                    )
                            sbcs += "k"
                        else:
                            if sbcs >= 1000:
                                sbcs = str((sbcs - (sbcs % 1000)) / 1000)
                                if sbcs.count(".") > 0:
                                    if len(sbcs.split(".")[1]) > 1:
                                        sbcs = (
                                            sbcs.split(".")[0]
                                            + "."
                                            + sbcs.split(".")[1][0]
                                        )
                                sbcs += "k"
                    tmpe = tmpe.replace("INFO_A", str(sbcs) + " Online")
                    tmpe = tmpe.replace("pVX", str(random.randint(0, 100))).replace(
                        "pVY", str(random.randint(0, 100))
                    )
                    tmpe = tmpe.replace(
                        "IMAGE_SLOT",
                        "background-image:url('" + tar.get("iconUrl") + "')",
                    )
                    tmpe = tmpe.replace("site_icon.png", "discord.png")
                    tmpe = tmpe.replace("PLATFORM_COLOR", "(115, 138, 219)")
                if platform == "twitch" and len(search_data.get("twitch_users")) > 1:
                    tar = search_data.get("twitch_users")[
                        random.randint(0, len(search_data.get("twitch_users")) - 1)
                    ]
                    br = 0
                    while accountsbr.count(tar) > 0 and br < 15:
                        tar = search_data.get("twitch_users")[
                            random.randint(0, len(search_data.get("twitch_users")) - 1)
                        ]
                        br += 1
                    if br >= 13:
                        pls.remove(platform)
                        cards.append(get_video_to_add(tmpe, search_data))
                        continue
                    accountsbr.append(tar)
                    tmpe = tmpe.replace(
                        "USER_TITLE",
                        str(
                            tar.get("screen_name")[
                                : min(
                                    len(tar.get("screen_name")), len("PepoBets | CSGO")
                                )
                            ].encode("ascii", "ignore")
                        )[2:-1],
                    )
                    tmpe = tmpe.replace(
                        "images/PLATFORM_NAME.png", tar.get("thumbnail")
                    )
                    tmpe = tmpe.replace("PLATFORM_NAME", "Twitch")
                    body_fill = (
                        tar.get("description")
                        .replace("/", " / ")
                        .replace(",", " , ")
                        .replace("  ", " ")
                        .replace(" ,", ",")
                    )
                    cut_off_length = len(
                        "The Scrimmage official discord server: Features: Sports / Sports betting chats Bots that bring in schedules, odds, trends, and both team and player stats. Live New"
                    )
                    if len(body_fill) > cut_off_length:
                        body_fill = body_fill[:cut_off_length] + "..."
                    tmpe = tmpe.replace("BODY_FILL", body_fill)
                    sbcs = int(tar.get("followers"))
                    if sbcs >= 1000000:
                        sbcs = str((sbcs - (sbcs % 100000)) / 1000000) + "m"
                    else:
                        if sbcs >= 100000:
                            sbcs = str((sbcs - (sbcs % 1000)) / 100000)
                            if sbcs.count(".") > 0:
                                if len(sbcs.split(".")[1]) > 1:
                                    sbcs = (
                                        sbcs.split(".")[0] + "." + sbcs.split(".")[1][0]
                                    )
                            sbcs += "k"
                        else:
                            if sbcs >= 1000:
                                sbcs = str((sbcs - (sbcs % 1000)) / 1000)
                                if sbcs.count(".") > 0:
                                    if len(sbcs.split(".")[1]) > 1:
                                        sbcs = (
                                            sbcs.split(".")[0]
                                            + "."
                                            + sbcs.split(".")[1][0]
                                        )
                                sbcs += "k"
                    tmpe = tmpe.replace("INFO_A", str(sbcs) + " Followers")
                    tmpe = tmpe.replace("pVX", str(random.randint(0, 100))).replace(
                        "pVY", str(random.randint(0, 100))
                    )
                    tmpe = tmpe.replace(
                        "IMAGE_SLOT",
                        "background-image:url('" + tar.get("thumbnail") + "')",
                    )
                    tmpe = tmpe.replace("site_icon.png", "twitch.png")
                    tmpe = tmpe.replace("PLATFORM_COLOR", "(160, 65, 165)")
                    tmpe = tmpe.replace("TARGET_URL", tar.get("link"))
                if platform == "youtube":
                    tar = search_data.get("youtube_data").get("channels")[
                        random.randint(
                            0, len(search_data.get("youtube_data").get("channels")) - 1
                        )
                    ]
                    br = 0
                    while (
                        accountsbr.count(tar) > 0
                        and br < 15
                        and int(tar.get("subscribers")) > 3000000
                    ):
                        tar = search_data.get("youtube_data").get("channels")[
                            random.randint(
                                0,
                                len(search_data.get("youtube_data").get("channels"))
                                - 1,
                            )
                        ]
                        br += 1
                    if br >= 13:
                        pls.remove(platform)
                        cards.append(get_video_to_add(tmpe, search_data))
                        continue
                    accountsbr.append(tar)
                    tmpe = tmpe.replace(
                        "USER_TITLE",
                        str(
                            tar.get("title")[
                                : min(len(tar.get("title")), len("PepoBets | CSGO"))
                            ].encode("ascii", "ignore")
                        )[2:-1],
                    )
                    tmpe = tmpe.replace(
                        "images/PLATFORM_NAME.png", tar.get("thumbnail").get("url")
                    )
                    tmpe = tmpe.replace("site_icon.png", "youtube.png")
                    tmpe = tmpe.replace("PLATFORM_NAME", "Youtube")
                    tmpe = tmpe.replace("PLATFORM_COLOR", "(255, 1, 1)")
                    sbcs = int(tar.get("subscribers"))
                    if sbcs >= 1000000:
                        sbcs = str((sbcs - (sbcs % 100000)) / 1000000) + "m"
                    else:
                        if sbcs >= 100000:
                            sbcs = str((sbcs - (sbcs % 1000)) / 100000)
                            if sbcs.count(".") > 0:
                                if len(sbcs.split(".")[1]) > 1:
                                    sbcs = (
                                        sbcs.split(".")[0] + "." + sbcs.split(".")[1][0]
                                    )
                            sbcs += "k"
                    body_fill = (
                        tar.get("description")
                        .replace("/", " / ")
                        .replace(",", " , ")
                        .replace("  ", " ")
                        .replace(" ,", ",")
                    )
                    cut_off_length = len(
                        "The Scrimmage official discord server: Features: Sports / Sports betting chats Bots that bring in schedules, odds, trends, and both team and player stats. Live New"
                    )
                    if len(body_fill) > cut_off_length:
                        body_fill = body_fill[:cut_off_length] + "..."
                    tmpe = tmpe.replace("BODY_FILL", body_fill)
                    tmpe = tmpe.replace("INFO_A", str(sbcs) + " Subs")
                    tmpe = tmpe.replace(
                        "TARGET_URL", "https://www.youtube.com/channel/" + tar.get("id")
                    )
                if platform == "twitter":
                    tar = search_data.get("twitter_users").get("accounts")[
                        random.randint(
                            0, len(search_data.get("twitter_users").get("accounts")) - 1
                        )
                    ]
                    br = 0
                    while accountsbr.count(tar) > 0 and br < 31:
                        tar = search_data.get("twitter_users").get("accounts")[
                            random.randint(
                                0,
                                len(search_data.get("twitter_users").get("accounts"))
                                - 1,
                            )
                        ]
                        br += 1
                    if br >= 31:
                        pls.remove(platform)
                        cards.append(get_video_to_add(tmpe, search_data))
                        continue
                    accountsbr.append(tar)
                    tmpe = tmpe.replace(
                        "USER_TITLE",
                        str(
                            tar.get("username")[
                                : min(len(tar.get("username")), len("PepoBets | CSGO"))
                            ].encode("ascii", "ignore")
                        )[2:-1],
                    )
                    tmpe = tmpe.replace(
                        "images/PLATFORM_NAME.png", tar.get("profile_image_url_https")
                    )
                    tmpe = tmpe.replace("PLATFORM_NAME", "Twitter")
                    tmpe = tmpe.replace("site_icon.png", "twitter.png")
                    tmpe = tmpe.replace("TARGET_URL", tar.get("link"))
                    sbcs = int(tar.get("followers_count"))
                    if sbcs >= 1000000:
                        sbcs = str((sbcs - (sbcs % 100000)) / 1000000) + "m"
                    else:
                        if sbcs >= 100000:
                            sbcs = str((sbcs - (sbcs % 1000)) / 100000)
                            if sbcs.count(".") > 0:
                                if len(sbcs.split(".")[1]) > 1:
                                    sbcs = (
                                        sbcs.split(".")[0] + "." + sbcs.split(".")[1][0]
                                    )
                            sbcs += "k"
                        else:
                            if sbcs >= 1000:
                                sbcs = str((sbcs - (sbcs % 1000)) / 1000)
                                if sbcs.count(".") > 0:
                                    if len(sbcs.split(".")[1]) > 1:
                                        sbcs = (
                                            sbcs.split(".")[0]
                                            + "."
                                            + sbcs.split(".")[1][0]
                                        )
                                sbcs += "k"
                    body_fill = (
                        tar.get("description")
                        .replace("/", " / ")
                        .replace(",", " , ")
                        .replace("  ", " ")
                        .replace(" ,", ",")
                    )
                    cut_off_length = len(
                        "The Scrimmage official discord server: Features: Sports / Sports betting chats Bots that bring in schedules, odds, trends, and both team and player stats. Live New"
                    )
                    if len(body_fill) > cut_off_length:
                        body_fill = body_fill[:cut_off_length] + "..."
                    tmpe = tmpe.replace("BODY_FILL", body_fill)
                    tmpe = tmpe.replace("INFO_A", str(sbcs) + " Followers")
                    tmpe = tmpe.replace("PLATFORM_COLOR", "(29,161,242)")
                cards.append(tmpe.replace(".0k", "k"))
            except:
                cards.append(get_video_to_add(tmpe, search_data))
        rows.append(card_rows.replace("CARD_FILL", "\n".join(cards)))

    return open("search.html", "r").read().replace("RESULTS_FILL", "<br>".join(rows))


def get_video_to_add(tmpe, search_data):
    tmpe = (
        open("card.html", "r")
        .read()
        .replace("WIDTH_DIMENSION", str(card_result_dimensions(3)[0]))
        .replace("MARGIN_DIMENSION", str(card_result_dimensions(3)[1]))
    )
    tar = search_data.get("youtube_data").get("channels")[
        random.randint(0, len(search_data.get("youtube_data").get("channels")) - 1)
    ]
    tmpe = tmpe.replace(
        "USER_TITLE",
        str(
            tar.get("title")[
                : min(len(tar.get("title")), len("PepoBets | CSGO"))
            ].encode("ascii", "ignore")
        )[2:-1],
    )
    tmpe = tmpe.replace("images/PLATFORM_NAME.png", tar.get("thumbnail").get("url"))
    tmpe = tmpe.replace("site_icon.png", "youtube.png")
    tmpe = tmpe.replace(
        "TARGET_URL", "https://www.youtube.com/channel/" + tar.get("id")
    )
    tmpe = tmpe.replace("PLATFORM_NAME", "Youtube")
    tmpe = tmpe.replace("PLATFORM_COLOR", "(255, 1, 1)")
    sbcs = int(tar.get("subscribers"))
    if sbcs >= 1000000:
        sbcs = str((sbcs - (sbcs % 100000)) / 1000000) + "m"
    else:
        if sbcs >= 100000:
            sbcs = str((sbcs - (sbcs % 1000)) / 100000)
            if sbcs.count(".") > 0:
                if len(sbcs.split(".")[1]) > 1:
                    sbcs = sbcs.split(".")[0] + "." + sbcs.split(".")[1][0]
            sbcs += "k"
    body_fill = (
        tar.get("description")
        .replace("/", " / ")
        .replace(",", " , ")
        .replace("  ", " ")
        .replace(" ,", ",")
    )
    cut_off_length = len(
        "The Scrimmage official discord server: Features: Sports / Sports betting chats Bots that bring in schedules, odds, trends, and both team and player stats. Live New"
    )
    if len(body_fill) > cut_off_length:
        body_fill = body_fill[:cut_off_length] + "..."
    tmpe = tmpe.replace("BODY_FILL", body_fill)
    tmpe = tmpe.replace("INFO_A", str(sbcs) + " Subs")
    return tmpe


def card_result_dimensions(card_count):
    return [82 / card_count, 7 / card_count]


app.run()

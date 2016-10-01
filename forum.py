#!/usr/bin/python3
import sopel.module
import sopel.formatting
import feedparser
import threading
import json
import os

url = "http://hannover.freifunk.net/forum/syndication.php?limit=15"
save_file = os.path.expanduser("~/.sopel/seen_forum_posts.json")
channel = None

seen = []

# we wan't to avoid multipostings, so we lock this mutex
mutex = threading.Semaphore(1)

try:
    with open(save_file, "r") as f:
        seen = json.loads(f.read())
except FileNotFoundError:
    print("save_file {} not found.".format(save_file))

def configure(config):
    # TODO: add configuration possibility
    pass

def setup(bot):
    global channel, url
    channel = bot.config.freifunkh.channel
    if channel is None:
        print("warning: you need to specify freifunkh.channel in your config")


@sopel.module.interval(60)
def check_forum_every_one_min(bot):
    global seen, mutex
    mutex.acquire()
    if channel in bot.channels:
        feed = feedparser.parse(url)

        count = 0
        new = False
        for entry in feed.entries:
            if count >= 5:
                break

            banner = sopel.formatting.color(
                    "[Forum]",
                    fg=sopel.formatting.colors.PINK
                    )
            if not entry.link in seen:
                new = True
                bot.msg(channel, "{0} Neues Thema: \"{1.title}\" - {1.link}".format(banner, entry))
                seen += [entry.link]
                count += 1

        if new:
            with open(save_file, "w") as f:
                f.write(json.dumps(seen))
    else:
        print("warning: module forum is enabled, but bot is not in channel %s" % channel )

    mutex.release()

import requests
import podcastparser
from feedgen.feed import FeedGenerator
import email.utils
from io import BytesIO

SOURCE_FEED = "https://api.mujrozhlas.cz/rss/podcast/f4133d64-ccb2-30e7-a70f-23e9c54d8e76.rss"
MIN_DURATION_SECONDS = 20 * 60  # 20 minutes

def build_filtered_feed():
    # Fetch and parse podcast RSS feed
    response = requests.get(SOURCE_FEED)
    parsed_feed = podcastparser.parse(SOURCE_FEED, BytesIO(response.content))
   
    # Filter entries by duration
    filtered_entries = [
        entry for entry in parsed_feed["episodes"]
        if entry.get("duration", 0) >= MIN_DURATION_SECONDS
    ]

    # Build new RSS feed
    fg = FeedGenerator()
    fg.title(parsed_feed["title"])
    fg.link(href=parsed_feed.get("link", ""), rel="alternate")
    fg.description(parsed_feed.get("description", ""))

    for entry in filtered_entries:
        fe = fg.add_entry()
        fe.title(entry["title"])
        fe.link(href=entry["link"])
        fe.guid(entry.get("id", entry["link"]))
        fe.pubDate(email.utils.format_datetime(entry["published"]))
        fe.description(entry.get("summary", ""))

        enclosure = entry.get("enclosure")
        if enclosure:
            fe.enclosure(
                enclosure["url"],
                str(enclosure.get("length", 0)),
                enclosure.get("type", "audio/mpeg")
            )

    # Save to file
    fg.rss_file("rss.xml")

if __name__ == "__main__":
    build_filtered_feed()

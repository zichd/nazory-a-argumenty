# Import required libraries

import email.utils  # For formatting datetimes into proper RFC-822 pubDate strings
import re
import sys
from datetime import datetime, timezone
from io import (
    BytesIO,  # To wrap raw bytes in a file-like object (needed for podcastparser)
)

import podcastparser  # For parsing podcast RSS feeds into structured Python dictionaries
import requests  # For fetching the RSS feed over HTTP
from feedgen.feed import (
    FeedGenerator,  # For generating RSS feeds in a high-level, easy way
)

# URL of the source podcast RSS feed you want to filter
SOURCE_FEED = (
    "https://api.mujrozhlas.cz/rss/podcast/f4133d64-ccb2-30e7-a70f-23e9c54d8e76.rss"
)

# Minimum episode duration to keep (in seconds); here set to 20 minutes
MIN_DURATION_SECONDS = 20 * 60


def build_filtered_feed():
    # STEP 1: Download the original RSS feed
    response = requests.get(
        SOURCE_FEED
    )  # Send a GET request to fetch the RSS feed content

    # STEP 2: Parse the downloaded RSS feed into a structured format
    # podcastparser requires a file-like object for the feed content, so we use BytesIO
    parsed_feed = podcastparser.parse(SOURCE_FEED, BytesIO(response.content))

    # STEP 3: Filter episodes by duration (only keep those >= 20 minutes)
    # Each episode is a dictionary with metadata like title, link, duration, enclosure, etc.
    filtered_entries = [
        entry
        for entry in parsed_feed["episodes"]
        if entry.get("total_time", 0) >= MIN_DURATION_SECONDS
    ]

    # STEP 4: Initialize a new RSS feed using FeedGenerator
    fg = FeedGenerator()
    fg.load_extension("podcast")  # enables podcast-specific RSS tags
    

    fg.title(parsed_feed["title"])
    fg.link(href=parsed_feed.get("link", ""), rel="alternate")
    fg.description(parsed_feed.get("description", ""))
    fg.image(
        url="https://portal.rozhlas.cz/sites/default/files/styles/mr_square_large/public/images/6c6fb3f7c59d454cd0a6cf28642ade7a.png?itok=RE3Eqiwx&v=3"
    )
    fg.language(parsed_feed.get("language", "cs"))
    fg.podcast.itunes_author(parsed_feed.get("itunes_author", "Unknown"))
    fg.podcast.itunes_image(parsed_feed.get("cover_url", ""))

    fg.podcast.itunes_explicit("no")
    fg.podcast.itunes_summary(parsed_feed.get("description", ""))

    # STEP 5: Add each filtered episode as an <item> to the new RSS feed
    for ep in filtered_entries:
        ep_enclousures = ep.get("enclosures", [{}])
        ep_enclousure = ep_enclousures[0]
        ep_enclousure_url = ep_enclousure.get("url", "")
        ep_enclousure_file_size = ep_enclousure.get("file_size", "")
        ep_enclousure_mime_type = ep_enclousure.get("mime_type", "")

        fe = fg.add_entry()  # Create a new <item> element

        # Add required metadata to each item
        fe.id(ep["guid"])
        fe.title(ep["title"])  # Episode title
        fe.description(ep["description"])
        fe.enclosure(
            ep_enclousure_url, ep_enclousure_file_size, ep_enclousure_mime_type
        )
        fe.podcast.itunes_duration(ep["total_time"])
        fe.pubDate(datetime.fromtimestamp(ep["published"], tz=timezone.utc))

    # fe.pubDate(ep["pubDate"])

    # STEP 6: Write the new RSS feed to a file named rss.xml
    # Generate pretty-printed XML as bytes
    rss_pretty = fg.rss_str(pretty=True).decode("utf-8")
    rss_pretty = re.sub(r"<generator>.*?</generator>\s*", "", rss_pretty)
    # Write it to a file manually
    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(rss_pretty)


# If the script is executed directly (not imported), run the feed builder
if __name__ == "__main__":
    build_filtered_feed()

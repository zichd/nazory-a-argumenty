# Import required libraries

import requests  # For fetching the RSS feed over HTTP
import podcastparser  # For parsing podcast RSS feeds into structured Python dictionaries
from feedgen.feed import FeedGenerator  # For generating RSS feeds in a high-level, easy way
import email.utils  # For formatting datetimes into proper RFC-822 pubDate strings
from io import BytesIO  # To wrap raw bytes in a file-like object (needed for podcastparser)

# URL of the source podcast RSS feed you want to filter
SOURCE_FEED = "https://api.mujrozhlas.cz/rss/podcast/f4133d64-ccb2-30e7-a70f-23e9c54d8e76.rss"

# Minimum episode duration to keep (in seconds); here set to 20 minutes
MIN_DURATION_SECONDS = 20 * 60

def build_filtered_feed():
    # STEP 1: Download the original RSS feed
    response = requests.get(SOURCE_FEED)  # Send a GET request to fetch the RSS feed content

    # STEP 2: Parse the downloaded RSS feed into a structured format
    # podcastparser requires a file-like object for the feed content, so we use BytesIO
    parsed_feed = podcastparser.parse(SOURCE_FEED, BytesIO(response.content))

    # STEP 3: Filter episodes by duration (only keep those >= 20 minutes)
    # Each episode is a dictionary with metadata like title, link, duration, enclosure, etc.
    filtered_entries = [
        entry for entry in parsed_feed["episodes"]
        #if entry.get("duration", 0) >= MIN_DURATION_SECONDS
        if True
    ]

    # STEP 4: Initialize a new RSS feed using FeedGenerator
    fg = FeedGenerator()
    fg.title(parsed_feed["title"])  # Set the feed's title (e.g. "Názory a Argumenty")
    fg.link(href=parsed_feed.get("link", ""), rel="alternate")  # Set the website link of the podcast
    fg.description(parsed_feed.get("description", ""))  # Set the feed description

    # STEP 5: Add each filtered episode as an <item> to the new RSS feed
    for entry in filtered_entries:
        fe = fg.add_entry()  # Create a new <item> element

        # Add required metadata to each item
        fe.title(entry["title"])  # Episode title
        fe.link(href=entry["link"])  # Link to the episode
        fe.guid(entry.get("id", entry["link"]))  # Globally unique ID; fall back to link if ID missing
        fe.pubDate(email.utils.format_datetime(entry["published"]))  # Properly formatted pubDate
        fe.description(entry.get("summary", ""))  # Summary or description of the episode

        # Add the audio file enclosure (required for podcast clients)
        enclosure = entry.get("enclosure")
        if enclosure:
            fe.enclosure(
                enclosure["url"],  # URL to the audio file
                str(enclosure.get("length", 0)),  # File size in bytes (as string)
                enclosure.get("type", "audio/mpeg")  # MIME type (default to audio/mpeg)
            )

    # STEP 6: Write the new RSS feed to a file named rss.xml
    fg.rss_file("rss.xml")  # Saves the feed in RSS 2.0 format

# If the script is executed directly (not imported), run the feed builder
if __name__ == "__main__":
    build_filtered_feed()

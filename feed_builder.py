import feedparser
from datetime import timedelta
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
import requests

SOURCE_FEED = "https://api.mujrozhlas.cz/rss/podcast/f4133d64-ccb2-30e7-a70f-23e9c54d8e76.rss"
MIN_DURATION_SECONDS = 20 * 60  # 20 minut

def parse_duration(duration_str):
    parts = duration_str.split(":")
    parts = [int(p) for p in parts]
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        h, m, s = 0, parts[0], parts[1]
    elif len(parts) == 1:
        h, m, s = 0, 0, parts[0]
    else:
        return 0
    return h * 3600 + m * 60 + s

def build_filtered_feed():
    feed = feedparser.parse(SOURCE_FEED)
    filtered_entries = []

    for entry in feed.entries:
        duration = entry.get("itunes_duration") or entry.get("duration")
        if duration:
            seconds = parse_duration(duration)
            if seconds >= MIN_DURATION_SECONDS:
                filtered_entries.append(entry)

    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")
    SubElement(channel, "title").text = "Názory a Argumenty"
    SubElement(channel, "link").text = feed.feed.link
    SubElement(channel, "description").text = feed.feed.get("description", "Podcast Českého rozhlasu – Názory a Argumenty")

    if "image" in feed.feed:
        image = SubElement(channel, "image")
        SubElement(image, "url").text = feed.feed.image.href
        SubElement(image, "title").text = "Názory a Argumenty"
        SubElement(image, "link").text = feed.feed.link

    for entry in filtered_entries:
        item = SubElement(channel, "item")
        SubElement(item, "title").text = entry.title
        SubElement(item, "link").text = entry.link
        SubElement(item, "guid").text = entry.id
        SubElement(item, "pubDate").text = entry.published
        SubElement(item, "description").text = entry.get("summary", "")
        enclosure = SubElement(item, "enclosure")
        enclosure.set("url", entry.enclosures[0].href)
        enclosure.set("type", entry.enclosures[0].type)
        enclosure.set("length", entry.enclosures[0].length if hasattr(entry.enclosures[0], "length") else "0")

    dom = xml.dom.minidom.parseString(tostring(rss, encoding="utf-8"))
    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(dom.toprettyxml(indent="  "))

if __name__ == "__main__":
    build_filtered_feed()

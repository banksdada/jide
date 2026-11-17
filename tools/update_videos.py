#!/usr/bin/env python3
"""Refresh videos.json from the public YouTube feed of Jide's channel.

Run by .github/workflows/update-videos.yml every few hours. You can also run it
by hand:  python3 tools/update_videos.py

If YouTube can't be reached or returns no videos, videos.json is left alone,
so the website never loses its list because of a bad run.
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

CHANNEL_ID = "UCyCuoStgyosDfWW4lr-FT1A"
FEED = "https://www.youtube.com/feeds/videos.xml?channel_id=" + CHANNEL_ID
OUT = Path(__file__).resolve().parent.parent / "videos.json"
MAX_VIDEOS = 12
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}


def parse(xml_bytes):
    root = ET.fromstring(xml_bytes)
    videos = []
    for entry in root.findall("a:entry", NS):
        vid = entry.findtext("yt:videoId", default="", namespaces=NS).strip()
        title = entry.findtext("a:title", default="", namespaces=NS).strip()
        published = entry.findtext("a:published", default="", namespaces=NS).strip()
        if vid:
            videos.append({"id": vid, "title": title, "published": published})
    return videos[:MAX_VIDEOS]


def main():
    try:
        req = urllib.request.Request(FEED, headers={"User-Agent": "Mozilla/5.0 (video list updater)"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            videos = parse(resp.read())
    except Exception as exc:  # network error, bad XML, etc.
        print("Could not read the YouTube feed:", exc)
        return 1
    if not videos:
        print("The feed had no videos, so videos.json was left unchanged.")
        return 1
    new_text = json.dumps(videos, indent=2, ensure_ascii=False) + "\n"
    old_text = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    if new_text == old_text:
        print("No new videos.")
        return 0
    OUT.write_text(new_text, encoding="utf-8")
    print("Updated videos.json with", len(videos), "videos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

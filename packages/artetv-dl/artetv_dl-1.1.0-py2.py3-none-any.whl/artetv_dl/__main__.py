#!/bin/python

"""A download a video from arte.tv website."""

from bs4 import BeautifulSoup
from urllib.request import urlopen, unquote, urlretrieve
import re, json, sys
import validators

def show_help(msg=None):
    if msg:
        print(msg)
    print("Usage:")
    print("    "+sys.argv[0]+" <arte.tv_link>")
    print("Example:")
    print("    "+sys.argv[0]+" https://www.arte.tv/fr/videos/051868-000-A/liberte-egalite-indemnites-vers-un-revenu-universel/")
    sys.exit(1)


def download(url):
    content = urlopen(url)
    json_data = json.loads(content.read().decode())
    name = json_data['videoJsonPlayer']['VTI']
    try:
        url = json_data['videoJsonPlayer']['VSR']['HTTPS_SQ_1']['url']
    except TypeError:
        print("Sorry, it seems that the video is no longer available.")
        sys.exit(0)

    name=name.replace('/', '-')+".mp4"
    try:
        print("Downloading '"+name+"'...")
        urlretrieve(url, name)
        print("\nDownload completed")
    except Exception as e:
        print(e)


def main():
    if len(sys.argv) != 2:
        show_help()

    url = sys.argv[1]

    if not validators.url(url):
        show_help("Error: This is not an url or maybe you forgot http(s):// before domain?")

    programId = re.findall('[0-9A-Z]{6}-[0-9A-Z]{3}-[0-9A-Z]', url)

    collection = re.findall('[0-9A-Z]{2}-[0-9A-Z]{6}', url)

    if len(programId) > 0:
        url = "https://api.arte.tv/api/player/v1/config/en/{}".format(programId[0])

        download(url)
    elif len(collection) > 0:
        content = urlopen(url)

        soup = BeautifulSoup(content, "lxml")

        links = soup.find_all("a", {"class": "next-teaser__link"}, href=True)

        for link in links:
            programId = re.findall('[0-9A-Z]{6}-[0-9A-Z]{3}-[0-9A-Z]', link['href'])
            url = "https://api.arte.tv/api/player/v1/config/en/{}".format(programId[0])
            download(url)

        if not links:
            url = "https://api.arte.tv/api/player/v1/collectionData/en/{}".format(collection[0])
            content = urlopen(url)
            json_data = json.loads(content.read().decode())
            videos = json_data['videos']
            for video in videos:
                url = "https://api.arte.tv/api/player/v1/config/en/{}".format(video['programId'])
                download(url)

    else:
        print("Error: Nothing found here, are your sure your are on arte.tv website and it's a valid video url?")
        show_help()


if __name__ == "__main__":
    main()

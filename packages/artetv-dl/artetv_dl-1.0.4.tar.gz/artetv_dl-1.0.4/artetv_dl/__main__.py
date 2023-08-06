#!/bin/python

"""A download a video from arte.tv website."""

from bs4 import BeautifulSoup
from urllib.request import urlopen, unquote, urlretrieve
import re, json, sys

def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("    "+sys.argv[0]+" <arte.tv_link>")
        print("Example:")
        print("    "+sys.argv[0]+" https://www.arte.tv/fr/videos/051868-000-A/liberte-egalite-indemnites-vers-un-revenu-universel/")
        sys.exit(0)

    url = sys.argv[1]

    programId = re.findall('[0-9A-Z]{6}-[0-9A-Z]{3}-[0-9A-Z]', url)[0]

    url = "https://api.arte.tv/api/player/v1/config/en/{}".format(programId)

    content = urlopen(url)
    json_data = json.loads(content.read().decode())
    name = json_data['videoJsonPlayer']['VTI']
    url = json_data['videoJsonPlayer']['VSR']['HTTPS_SQ_1']['url']

    name=name.replace('/', '-')+".mp4"
    try:
        print("Downloading '"+name+"'...")
        urlretrieve(url, name)
        print("\nDownload completed")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()

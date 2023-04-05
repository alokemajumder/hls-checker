# hls_checker.py

import requests
import m3u8
import sys

def get_hls_url():
    url = input("Enter the target HLS URL: ")
    return url.strip()

def check_hls_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {url} is not accessible. Details: {e}")
        return

    try:
        playlist = m3u8.loads(response.text)
    except ValueError as e:
        print(f"Error: Unable to parse the playlist. Details: {e}")
        return

    if playlist.is_variant:
        print(f"Checking {len(playlist.playlists)} variant playlists...")
        for variant in playlist.playlists:
            check_hls_url(variant.absolute_uri)
    else:
        print(f"Checking {len(playlist.segments)} segments...")
        for segment in playlist.segments:
            try:
                segment_response = requests.head(segment.absolute_uri, timeout=5)
                segment_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error: Segment {segment.absolute_uri} is not accessible. Details: {e}")

if __name__ == "__main__":
    hls_url = get_hls_url()
    check_hls_url(hls_url)
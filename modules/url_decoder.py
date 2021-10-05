import requests, json

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}

def url_decode(href: str):
    try:
        r = requests.get(href, headers = headers)
        raw_url = r.url
        link_to_track = raw_url.split("?")[0]
        return link_to_track
    except: 
        return 0

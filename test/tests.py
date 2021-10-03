from sc import Soundcloud
import json, json_config, asyncio, requests
from urllib.parse import quote


import aiohttp

sc = Soundcloud()
config = json_config.connect('config.json')
text = quote('дора')

limit = 10
offset = 0


href = f'https://api-v2.soundcloud.com/search?q={text}&variant_ids=2382%2C2375&facet=model&client_id={config["sc_client_id"]}&limit={limit}&offset={offset}&linked_partitioning=1&app_version=1633082668&app_locale=en'
r = requests.get(href)

response = json.loads(r.text)
links = []
for item in response['collection']:
    if item['kind'] == "track":
        text = item['uri']
        links.append(text)


async def download(link):
        await sc.getTrack(link)



ioloop = asyncio.get_event_loop()
tasks = []
for link in links:

    tasks.append(ioloop.create_task(download(link)))

wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()


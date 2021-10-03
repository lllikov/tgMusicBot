
from sc import Soundcloud
import json, json_config, asyncio, requests
from urllib.parse import quote



sc = Soundcloud()
config = json_config.connect('config.json')
text = quote('дора')

href = f'https://api-v2.soundcloud.com/search?q={text}&variant_ids=2382%2C2375&facet=model&client_id={config["sc_client_id"]}&limit={limit}&offset={offset}&linked_partitioning=1&app_version=1633082668&app_locale=en'



r = requests.get(href)






# response = json.loads(r.text)
# array = []
# for item in response['collection']:
#     if item['kind'] == "track":
#         text = item['uri']
#         array.append(text)


# async def sss():
#     await sc.getTrack(array[1])


# if __name__ == "__main__":
#     asyncio.run(sss())
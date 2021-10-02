import requests
import soundcloud

import urllib3
import json
from urllib.parse import quote
client = soundcloud.Client(client_id="Z6ygXZr52uoKmSfsaK4ZpxFx1sAvSZ3n")
text = quote('дора')

href = f'https://api-v2.soundcloud.com/search?q=%D0%B4%D0%BE%D1%80%D0%B0&sc_a_id=4cdec31472c65cff3d0b41094074719b362c5537&variant_ids=2382%2C2375&facet=model&user_id=568482-737679-121123-876021&client_id=Z6ygXZr52uoKmSfsaK4ZpxFx1sAvSZ3n&limit=20&offset=0&linked_partitioning=1&app_version=1633082668&app_locale=en'

# headers = {
#     "accept": "application/json; charset=utf-8",
#     "Authorization": "2-292926-1031896816-T6q4ZDYLTYOFj"
# }

r = requests.get(href)

response = json.loads(r.text)
for item in response['collection']:
    if item['kind'] == "track":
        text = item['uri'].split('https://api.soundcloud.com')
        app = client.get(text[1])
        print(app)


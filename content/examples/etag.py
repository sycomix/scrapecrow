import requests
from time import time

url = "https://www.coindesk.com/"
last_known_version = None
session = requests.session()
_start = time()
for i in range(10):
    resp = session.head(url)
    current_version = resp.headers['etag']
    # new verison has been seen
    if current_version != last_known_version:
        resp = session.get(url)
        last_known_version = current_version
    else:  # nothing has ehcnaged
        continue
print(f"finished in {_start - time()}")



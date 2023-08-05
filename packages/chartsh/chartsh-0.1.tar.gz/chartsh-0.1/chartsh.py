"""Seamlessly uploading altair charts to chartsh.com"""

import requests
import json


__version__ = "0.1"


def upload(chart, title = "null", description = "null"):
    """ Upload chart publically to chartsh.com """
    url = "http://www.chartsh.com/ingest/submit/"
    data = {"json": chart.to_json(), "id": "null", "title": title, "description": description}
    page = requests.post(url = url, data = data)
    # print(page.content.decode("utf-8"))    
    return(page.content.decode("utf-8"))
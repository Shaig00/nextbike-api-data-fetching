from curl_cffi import requests
import os
from rich import print


def new_sessions():
    session = requests.Session(impersonate="chrome", proxy=os.getenv("stickyproxy"))
    return session

def fetch_api(session: requests.Session, url: str):
    URL = url
    resp = session.get(URL)
    resp.raise_for_status()
    return resp

def request_data(url):
    session = new_sessions()
    response = fetch_api(session=session, url=url)
    return response
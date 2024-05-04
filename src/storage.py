import os
import json
from config import config
import datetime

data_cache = {}

def get_timer_path():
    return f"{config.get("BASE_PATH")}/timers.json"

def read():
    global data_cache

    if not os.path.isfile(get_timer_path()):
        return
    
    data_cache.clear()
    with open(get_timer_path(), "r") as f:
        data_cache.update(json.load(f))

def write():
    global data_cache
    
    dir = os.path.dirname(get_timer_path())
    if not os.path.isdir(dir):
        os.makedirs(dir)

    with open(get_timer_path(), "w") as f:
        json.dump(data_cache, f)

def set_laundry_timer(name: str, curr_user: str, end_time: datetime.datetime):
    global data_cache
    data_cache.update({name:{"currUser": curr_user, "endTime": int(end_time.timestamp())}})
    write()

def get_laundry_timer(name: str) -> tuple[str, datetime.datetime]:
    data = data_cache.get(name)
    if data and data.get("currUser") and data.get("endTime"):
        return (data.get("currUser"), datetime.datetime.fromtimestamp(data.get("endTime")))
    return ("", None)

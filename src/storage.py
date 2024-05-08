import os
import json
from config import config
import datetime

timer_data_cache = {}
house_data_cache = {}

def get_timer_path():
    return f"{config.get("BASE_PATH")}/timers.json"

def get_alarm_path():
    return f"{config.get("BASE_PATH")}/alarms.txt"

def get_house_path():
    return f"{config.get("BASE_PATH")}/house.json"

def read_house():
    global house_data_cache

    if not os.path.isfile(get_house_path()):
        return
    
    house_data_cache.clear()
    with open(get_house_path(), "r") as f:
        house_data_cache.update(json.load(f))

def write_house(chat_id:int, house:str):
    global house_data_cache
    
    house_data_cache.update({chat_id:house})
    dir = os.path.dirname(get_house_path())
    if not os.path.isdir(dir):
        os.makedirs(dir)

    with open(get_house_path(), "w") as f:
        json.dump(house_data_cache, f)

def get_house(chat_id:int) -> str|None:
    return house_data_cache.get(str(chat_id))

def read_timers():
    global timer_data_cache

    if not os.path.isfile(get_timer_path()):
        return
    
    timer_data_cache.clear()
    with open(get_timer_path(), "r") as f:
        timer_data_cache.update(json.load(f))

def write_timers():
    global timer_data_cache
    
    dir = os.path.dirname(get_timer_path())
    if not os.path.isdir(dir):
        os.makedirs(dir)

    with open(get_timer_path(), "w") as f:
        json.dump(timer_data_cache, f)

def set_laundry_timer(machine_name: str, curr_user: str, end_time: datetime.datetime, chat_id: int):
    global timer_data_cache
    timestamp = int(end_time.timestamp())
    timer_data_cache.update({machine_name:{"currUser": curr_user, "endTime": timestamp}})
    write_timers()
    write_alarms(curr_user, timestamp, chat_id)

def get_laundry_timer(name: str) -> tuple[str, datetime.datetime]:
    data = timer_data_cache.get(name)
    if data and data.get("currUser") and data.get("endTime"):
        return (data.get("currUser"), datetime.datetime.fromtimestamp(data.get("endTime")))
    return ("", None)

def write_alarms(curr_user: str, end_timestamp: int, chat_id: int):
    with open(get_alarm_path(), "a") as f:
        f.write(f"{end_timestamp} | {curr_user} | {chat_id} \n")

def check_alarms() -> list[tuple[str, str, int]]:
    if not os.path.isfile(get_alarm_path()):
        return []
    
    with open(get_alarm_path(), "r+") as f:
        now = datetime.datetime.now().timestamp()
        rem_lines = []
        alarms = []
        lines = f.readlines()
        for line in lines:
            end_timestamp, curr_user, chat_id = line.split(" | ")
            if now > int(end_timestamp):
                alarms.append((curr_user, chat_id))
            else: 
                rem_lines.append(line)
        f.seek(0)
        f.truncate(0)
        f.write("".join(rem_lines))
        return alarms

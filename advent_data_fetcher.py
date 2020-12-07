import json, requests
from secret import LID_1, LID_2, LID_3
from datetime import datetime, timedelta
from global_vars import last_data_update, TEST_MODE, test_data, COOKIES, data
from data_classes import Member, Day

def fetch_data(year, leaderboard, force=False):
    global last_data_update
    now = datetime.now()
    if force or (year, leaderboard) not in last_data_update:
        print("  lb command... fetching data, none exists" if not force else "  lb command... FORCE FETCHING DATA")
        last_data_update[(year, leaderboard)] = now
        if get_json_data(year, leaderboard):
            update_data()
    elif (now - last_data_update[(year, leaderboard)]) > timedelta(minutes=15):
        print("  lb command... fetching data, 15 minutes has passed")
        if get_json_data(year, leaderboard):
            update_data()
    else:
        print("  lb command... using existing data, 15 minutes not passed")
    return data


def get_json_data(year, leaderboard):
    if leaderboard=="1":
        leaderboard = LID_1
    elif leaderboard=="2":
        leaderboard = LID_2
    elif leaderboard=="3":
        leaderboard = LID_3

    global json_data
    global data
    data = []
    if TEST_MODE:
        json_data = json.loads(test_data)
    else:
        url = "https://adventofcode.com/" + year + "/leaderboard/private/view/" + leaderboard + ".json"
        with requests.get(url, cookies=COOKIES) as response:
            html = response.text
            json_data = json.loads(html)

    return json_data

def update_data():
    global data
    for member_id in json_data["members"]:
        data.append(read_member(member_id))

def read_member(id):
    member = json_data["members"][id]
    name = member["name"]
    last_star_ts = member["last_star_ts"]
    score = member["local_score"]
    days = read_days(member["completion_day_level"])
    return Member(name, score, days, last_star_ts)

def read_days(days):
    days_output = {}
    for day_num in days:
        day = days[day_num]
        if "1" in day:
            part1 = day["1"]["get_star_ts"]
        else:
            continue
        if "2" in day:
            part2 = day["2"]["get_star_ts"]
        else:
            part2 = ''
        days_output[day_num] = Day(part1, part2)
    return days_output

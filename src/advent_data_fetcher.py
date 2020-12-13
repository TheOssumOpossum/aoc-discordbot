import json, requests
from datetime import datetime, timedelta
from constants import TEST_MODE, COOKIES, test_data, LID_1, LID_2, LID_3
from data_classes import Member, Day

data = {}

def fetch_data(year, leaderboard, last_data_update, force=False):
    global data
    now = datetime.now()
    if force or (year, leaderboard) not in last_data_update:
        print("  lb command... fetching data, none exists" if not force else "  lb command... FORCE FETCHING DATA")
        last_data_update[(year, leaderboard)] = now
        json_data = get_json_data(year, leaderboard)
        if json_data:
            data[leaderboard] = update_data(json_data, leaderboard)
    elif (now - last_data_update[(year, leaderboard)]) > timedelta(minutes=15):
        print("  lb command... fetching data, 15 minutes has passed")
        last_data_update[(year, leaderboard)] = now
        json_data = get_json_data(year, leaderboard)
        if json_data:
            data[leaderboard] = update_data(json_data, leaderboard)
    else:
        print("  lb command... using existing data, 15 minutes not passed")
    return data[leaderboard]

def get_json_data(year, leaderboard):
    if leaderboard=="1":
        leaderboard = LID_1
    elif leaderboard=="2":
        leaderboard = LID_2
    elif leaderboard=="3":
        leaderboard = LID_3

    if TEST_MODE:
        json_data = json.loads(test_data)
    else:
        url = "https://adventofcode.com/" + year + "/leaderboard/private/view/" + leaderboard + ".json"
        # url = "https://adventofcode.com/" + year + "/leaderboard/self"
        with requests.get(url, cookies=COOKIES) as response:
            html = response.text
            # print(html)
            json_data = json.loads(html)

    return json_data

def update_data(json_data, leaderboard):
    global data
    data[leaderboard] = []
    for member_id in json_data["members"]:
        data[leaderboard].append(read_member(member_id, json_data))
    return data[leaderboard]

def read_member(id, json_data):
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

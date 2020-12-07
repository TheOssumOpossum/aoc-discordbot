import json, datetime, requests, discord, pytz, tabulate, os
from discord.ext import tasks, commands
from contextlib import suppress
tabulate.PRESERVE_WHITESPACE = True
from utils import arg_parser
from secret import *
import timecog

YEAR = "2020"
DNF_STRING = "             DNF"
H24_STRING = "            >24h"
TIMEZONE = pytz.timezone("US/Eastern")
TEST_MODE = False

SECONDS_IN_A_DAY = 86400

COOKIES = {
    'session': os.environ.get('ADVENT_COOKIE', SESSION_COOKIE)
}
DISCORD_CLIENT_ID = os.environ.get('ADVENT_BOT_ID', DISCORD_CLIENT_ID)
LEADERBOARD = os.environ.get('LEADERBOARD', LEADERBOARD)

last_data_update = {}
test_data = ""
json_data = {}
data = []

class Member():
    name = ""
    score = 0
    days = {}
    last_star_ts = float("inf")
    def __init__(self, name, score, days, last_star_ts):
        self.name = name
        self.score = score
        self.days = days
        self.last_star_ts = last_star_ts

class Day():
    part1 = 0
    part2 = 0

    def __init__(self, part1, part2):
        self.part1 = part1
        self.part2 = part2

    def __str__(self):
        return "p1:{0} p2:{1}".format(self.part1, self.part2)

    def __repr__(self):
        return self.__str__()


# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('discordbot... Logged on as {0}!'.format(self.user))
#         await client.change_presence(status=discord.Status.invisible)

#     async def on_message(self, message):
#         if message.author.name != self.user.name:
#             print('discordbot... Message from {0.author}: {0.content}'.format(message))
#             await handle_message(message)


async def handle_message(message):
    content = message.content.lower()
    channel_name = message.channel.name
    if len(content) >= 100:
        print(" message_handler... ignoring long message from {0.author}".format(message))
        return
    if len(content) <= 1 or content[0] != '?':
        return
    command, *args = content[1:].split(' ')
    print(" message_handler... Received command:", command, "with args:", args)

    arg_ls, arg_dic = arg_parser(args)

    if channel_name == "advent-of-code-2020" and (command == "lb" or command == "leaderboard"):
        await handle_command_lb(arg_ls, arg_dic, message.channel)
    elif channel_name == "advent-of-code-2020" and (command == "help"):
        f = open("messages/help.txt",'r')
        help_msg = f.read()
        f.close()
        await send_message(help_msg, message.channel)
        await handle_command_lb(arg_ls, arg_dic, message.channel)
    elif channel_name == "advent-of-code-2020" and (command == "ping"):
        await send_message("pong", message.channel)
        await handle_command_lb(arg_ls, arg_dic, message.channel)
    elif channel_name == "advent-of-code-2020" and (command == "repo"):
        f = open("messages/help.txt",'r')
        help_msg = f.read()
        f.close()
        await send_message("`https://github.com/TheOssumOpossum/discordbot`", message.channel)

async def send_message(text, channel):
    await channel.send(text)

############### Fetching Data ################################

def fetch_data(force=False, year=YEAR, leaderboard=LEADERBOARD):
    global last_data_update
    now = datetime.datetime.now()
    if force or (year, leaderboard) not in last_data_update:
        print("  lb command... fetching data, none exists" if not force else "  lb command... FORCE FETCHING DATA")
        last_data_update[(year, leaderboard)] = now
        if get_json_data(year, leaderboard):
            update_data()
    elif (now - last_data_update[(year, leaderboard)]) > datetime.timedelta(minutes=15):
        print("  lb command... fetching data, 15 minutes has passed")
        if get_json_data(year, leaderboard):
            update_data()
    else:
        print("  lb command... using existing data, 15 minutes not passed")


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
        URL="https://adventofcode.com/" + year + "/leaderboard/private/view/" + leaderboard + ".json"
        with requests.get(URL, cookies=COOKIES) as response:
            html = response.text
            json_data = json.loads(html)

    return json_data

def update_data():
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

##################### Leaderboard command handler ###############################

#lb                 get todays leaderboard (short)
#lb n               get leaderboard for a certain day
#lb   --detailed    get todays leaderboard (long)
#lb n --detailed    get specific leaderboard for a day (long)

#-f force refresh data

async def handle_command_lb(arg_ls, arg_dic, channel):
    year = YEAR if "year" not in arg_dic else arg_dic["year"]
    leaderboard = LEADERBOARD if "leaderboard" not in arg_dic else arg_dic["leaderboard"]
    fetch_data("force" in arg_dic, year, leaderboard)

    if len(arg_ls) == 0:
        day = str(datetime.datetime.now(TIMEZONE).day)
        table = get_table(day)
        if "detailed" in arg_dic:
            #lb d
            message = print_full_lb_table(table, day, year, leaderboard)
        else:
            #lb
            message = print_short_lb_table(table, day, year, leaderboard)
    else:
        day = arg_ls[0]
        if int(day) > int(datetime.datetime.now(TIMEZONE).day):
            await send_message("```I can't see into the future```", channel)
            return
        table = get_table(day,sorter="today_score")
        if "detailed" in arg_dic:
            #lb 1 d
            message = print_full_lb_table_specific_day(table, day, year, leaderboard)
        else:
            #lb 1
            message = print_short_lb_table_specific_day(table, day, year, leaderboard)

    await send_message(message, channel)

################### Get Table ##########################

def get_table(day, sorter="local_score"):
    table = populate_table(day, sorter)
    assign_ranks(table, sorter)
    assign_rank_delta(table, day)
    return table

def populate_table(day, sorter):
    table = []
    for member in data:
        row = get_member_columns(member, day)
        table.append(row)
    if sorter == "local_score":
        table = sorted(table, key=lambda row: (row[2], -float(row[-2])), reverse=True)
    elif sorter == "today_score":
        table = sorted(table, key=lambda row: (int(row[9]), int(row[7])), reverse=True)
    return table

def assign_rank_delta(table, day):
    if day != 1:
        old_ranks = get_old_ranks(table)
        for row in table:
            row[1] = old_ranks[row[3]] - row[0]
            if row[1] > 0:
                row[1] = "+" + str(row[1])

def get_old_ranks(table):
    old_points = get_old_points(table)
    old_ranks = {}
    cur_score = float("inf")
    cur_rank = 0
    buffer = 1
    for member in old_points:
        score = member[0]
        if score < cur_score:
            cur_rank += buffer
            buffer = 1
            cur_score = score
        else:
            buffer += 1
        old_ranks[member[1]] = cur_rank
    return old_ranks

def get_old_points(table):
    old_points = []
    for row in table:
        score = 0
        if len(str(row[5])) != 1:
            score = int(str(row[5])[1:])
        old_points.append((row[2]-score,row[3]))
    return sorted(old_points, key=lambda x: x[0], reverse=True)

def assign_ranks(table, sorter):
    if sorter == "local_score":
        comparison_index = 2
    else:
        comparison_index = 9

    cur_score = float("inf")
    cur_rank = 0
    buffer = 1
    for member in table:
        score = int(member[comparison_index])
        if score < cur_score:
            cur_rank += buffer
            buffer = 1
            cur_score = score
        else:
            buffer += 1
        member[0] = cur_rank

def get_member_columns(member, day):
    row = []

    rank = 0
    prev_rank = 0
    rank_delta = 0
    score = member.score
    name = member.name
    completion_time = get_completion_time(member, day)
    part1 = get_part1_time(member, day)
    part2 = get_part2_time(member, day)
    last_star_ts = member.last_star_ts

    times1 = get_times_for_day_part1(day)
    points1 = get_points1(member, day, times1)

    times2 = get_times_for_day_part2(day)
    points2 = get_points2(member, day, times2)

    score_delta = points1 + points2
    if score_delta > 0:
        score_delta = "+" + str(score_delta)
    if points1 > 0:
        points1 = "+" + str(points1)
    if points2 > 0:
        points2 = "+" + str(points2)

    row.append(rank)
    row.append(rank_delta)
    row.append(score)
    row.append(name)
    row.append(completion_time)
    row.append(score_delta)
    row.append(part1)
    row.append(points1)
    row.append(part2)
    row.append(points2)
    row.append(last_star_ts)
    row.append(prev_rank)

    return row

def get_completion_time(member, day):
    if day in member.days and member.days[day].part2:
        ticks = float(member.days[day].part2)
        release_time = datetime.datetime(int(YEAR),12,int(day),0,0,0,0) + datetime.timedelta(hours=5)
        completion_time = datetime.datetime.utcfromtimestamp(ticks) - release_time
        return format_completion_time(completion_time)
    else:
        return DNF_STRING

def get_part1_time(member, day):
    if day in member.days and member.days[day].part1:
        ticks = float(member.days[day].part1)
        release_time = datetime.datetime(int(YEAR),12,int(day),0,0,0,0) + datetime.timedelta(hours=5)
        completion_time = datetime.datetime.utcfromtimestamp(ticks) - release_time
        return format_completion_time(completion_time)
    else:
        return DNF_STRING

def get_part2_time(member, day):
    if day in member.days and member.days[day].part2:
        ticks1 = float(member.days[day].part1)
        ticks2 = float(member.days[day].part2)
        release_time = datetime.datetime.utcfromtimestamp(ticks1)
        completion_time = datetime.datetime.utcfromtimestamp(ticks2) - release_time
        return format_completion_time(completion_time)
    else:
        return DNF_STRING

def format_completion_time(completion_time):
    if completion_time.total_seconds() >= SECONDS_IN_A_DAY:
        return H24_STRING
    else:
        if len(str(completion_time)) == 7:
            return "        0" + str(completion_time)
        else:
            return "        " + str(completion_time)

def get_points1(member, day, times):
    if day in member.days:
        score = len(times)
        finish_time = member.days[day].part1
        i = 0
        while times[i] != finish_time:
            i += 1
            score -= 1
        return score
    else:
        return 0

def get_points2(member, day, times):
    if day in member.days and member.days[day].part2:
        score = len(times)
        finish_time = member.days[day].part2
        i = 0
        while times[i] != finish_time:
            i += 1
            score -= 1
        return score
    else:
        return 0

def get_times_for_day_part1(day):
    times = []
    for member in data:
        if day in member.days:
            times.append(member.days[day].part1)
    times.sort()
    return times

def get_times_for_day_part2(day):
    times = []
    for member in data:
        if day in member.days and member.days[day].part2:
            times.append(member.days[day].part2)
    times.sort()
    return times

########################## PRINT TABLES ####################################

def print_full_lb_table(table, day, year, leaderboard):
    table_str = []
    for row in table:
        table_str.append(row[:-2])
    table_str = tabulate.tabulate(table_str, headers=["#", "+-", "Score", "Name", "CompletionTime", "pts", "Part1", "pts", "Part2", "pts"])
    return add_header_footer(table_str, day, year, leaderboard)

def print_short_lb_table(table, day, year, leaderboard):
    table_str = []
    for row in table:
        table_str.append(row[:-6])
    table_str = tabulate.tabulate(table_str, headers=["#", "+-", "Score", "Name", "CompletionTime", "pts"])
    return add_header_footer(table_str, day, year, leaderboard)

def print_short_lb_table_specific_day(table, day, year, leaderboard):
    table_str = []
    for row in table:
        if row[4] != DNF_STRING:
            table_str.append([row[0]] + row[3:-6])
    table_str = tabulate.tabulate(table_str, headers=["#", "Name", "CompletionTime", "pts"])
    return add_header_footer(table_str, day, year, leaderboard)

def print_full_lb_table_specific_day(table, day, year, leaderboard):
    table_str = []
    for row in table:
        if row[4] != DNF_STRING:
            table_str.append([row[0]] + row[3:-2])
    table_str = tabulate.tabulate(table_str, headers=["#", "Name", "CompletionTime", "pts", "Part1", "pts", "Part2", "pts"])
    return add_header_footer(table_str, day, year, leaderboard)

def add_header_footer(table, day, year, leaderboard):
    minutes, seconds = divmod((datetime.datetime.now() - last_data_update[(year,leaderboard)]).total_seconds(), 60)
    minutes = int(minutes)
    seconds = int(seconds)
    if seconds == 0:
        daystr = "Day {0}     (last updated now)\n".format(day)
    else:
        daystr = "Day {0}     (last updated {1}{2}{3}seconds ago)\n".format(day, "" if minutes == 0 else minutes, "" if minutes == 0 else "minute " if minutes == 1 else "minutes ", seconds)
    header = "```\n" + daystr
    footer = "\n```"
    return header + table + footer

###

def get_channel(channels, channel_name):
    for channel in client.get_all_channels():
        print(channel)
        if channel.name == channel_name:
            return channel
    return None


async def on_ready():
    print('discordbot... Logged on as {0}!'.format(client.user))
    await client.change_presence(status=discord.Status.invisible)

async def on_message(message):
    if message.author.name != client.user.name:
        print('discordbot... Message from {0.author}: {0.content}'.format(message))
    await handle_message(message)

# client = MyClient(status="dnd")
client = commands.Bot(command_prefix=commands.when_mentioned_or('~'))
client.add_listener(on_ready)
client.add_listener(on_message)
client.load_extension('timecog')

client.run(DISCORD_CLIENT_ID)

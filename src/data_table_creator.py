import datetime
from constants import YEAR, DNF_STRING, H24_STRING, DNF_STRING, SECONDS_IN_A_DAY

def get_table(day, data, sorter="local_score"):
    table = populate_table(day, data, sorter)
    assign_ranks(table, sorter)
    assign_rank_delta(table, day)
    return table

def populate_table(day, data, sorter):
    table = []
    for member in data:
        row = get_member_columns(member, day, data)
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

def get_member_columns(member, day, data):
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

    times1 = get_times_for_day_part1(day, data)
    points1 = get_points1(member, day, times1)

    times2 = get_times_for_day_part2(day, data)
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

def get_times_for_day_part1(day, data):
    times = []
    for member in data:
        if day in member.days:
            times.append(member.days[day].part1)
    times.sort()
    return times

def get_times_for_day_part2(day, data):
    times = []
    for member in data:
        if day in member.days and member.days[day].part2:
            times.append(member.days[day].part2)
    times.sort()
    return times

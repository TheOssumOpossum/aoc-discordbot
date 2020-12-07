import tabulate
from datetime import datetime
from global_vars import DNF_STRING

def print_full_lb_table(table, day, year, leaderboard, last_data_update):
    table_str = []
    for row in table:
        table_str.append(row[:-2])
    table_str = tabulate.tabulate(table_str, headers=["#", "+-", "Score", "Name", "CompletionTime", "pts", "Part1", "pts", "Part2", "pts"])
    return add_header_footer(table_str, day, year, leaderboard, last_data_update)

def print_short_lb_table(table, day, year, leaderboard, last_data_update):
    table_str = []
    for row in table:
        table_str.append(row[:-6])
    table_str = tabulate.tabulate(table_str, headers=["#", "+-", "Score", "Name", "CompletionTime", "pts"])
    return add_header_footer(table_str, day, year, leaderboard, last_data_update)

def print_short_lb_table_specific_day(table, day, year, leaderboard, last_data_update):
    table_str = []
    for row in table:
        if row[4] != DNF_STRING:
            table_str.append([row[0]] + row[3:-6])
    table_str = tabulate.tabulate(table_str, headers=["#", "Name", "CompletionTime", "pts"])
    return add_header_footer(table_str, day, year, leaderboard, last_data_update)

def print_full_lb_table_specific_day(table, day, year, leaderboard, last_data_update):
    table_str = []
    for row in table:
        if row[6] != DNF_STRING:
            table_str.append([row[0]] + row[3:-2])
    table_str = tabulate.tabulate(table_str, headers=["#", "Name", "CompletionTime", "pts", "Part1", "pts", "Part2", "pts"])
    return add_header_footer(table_str, day, year, leaderboard, last_data_update)

def add_header_footer(table, day, year, leaderboard, last_data_update):
    minutes, seconds = divmod((datetime.now() - last_data_update[(year,leaderboard)]).total_seconds(), 60)
    minutes = int(minutes)
    seconds = int(seconds)
    if seconds == 0:
        daystr = "Day {0}     (last updated now)\n".format(day)
    else:
        daystr = "Day {0}     (last updated {1}{2}{3}seconds ago)\n".format(day, "" if minutes == 0 else minutes, "" if minutes == 0 else "minute " if minutes == 1 else "minutes ", seconds)
    header = "```\n" + daystr
    footer = "\n```"
    return header + table + footer

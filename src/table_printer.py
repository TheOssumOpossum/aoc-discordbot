import tabulate
from datetime import datetime
from constants import DNF_STRING
from table_col_constants import *
tabulate.PRESERVE_WHITESPACE = True

def print_full_lb_table(table, day, year, leaderboard, last_data_update):
    table_str = []
    for row in table:
        table_str.append(row[:PART2_POINTS_COL+1])
    table_str = tabulate.tabulate(table_str, headers=["#", "+-", "Score", "Name", "CompletionTime", "pts", "Part1", "pts", "Part2", "pts"])
    return add_header_footer(table_str, day, year, leaderboard, last_data_update)

def print_short_lb_table(table, day, year, leaderboard, last_data_update):
    table_str = []
    for row in table:
        table_str.append(row[:TOTAL_POINTS_COL+1])
    table_str = tabulate.tabulate(table_str, headers=["#", "+-", "Score", "Name", "CompletionTime", "pts"])
    return add_header_footer(table_str, day, year, leaderboard, last_data_update)

def print_short_lb_table_specific_day(table, day, year, leaderboard, last_data_update):
    table_str = []
    for row in table:
        if row[TOTAL_TIME_COL] != DNF_STRING:
            table_str.append([row[RANK_COL]] + row[NAME_COL:TOTAL_POINTS_COL+1])
    table_str = tabulate.tabulate(table_str, headers=["#", "Name", "CompletionTime", "pts"])
    return add_header_footer(table_str, day, year, leaderboard, last_data_update)

def print_full_lb_table_specific_day(table, day, year, leaderboard, last_data_update):
    table_str = []
    for row in table:
        if row[PART2_TIME_COL] != DNF_STRING:
            table_str.append([row[RANK_COL]] + row[NAME_COL:PART2_POINTS_COL+1])
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

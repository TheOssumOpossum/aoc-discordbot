import table_printer
from constants import YEAR, LEADERBOARD, TIMEZONE
from advent_data_fetcher import fetch_data
from datetime import datetime
from data_table_creator import get_table
from discord_api import send_message

#lb                 get todays leaderboard (short)
#lb n               get leaderboard for a certain day
#lb   --detailed    get todays leaderboard (long)
#lb n --detailed    get specific leaderboard for a day (long)

#-f force refresh data

async def handle_command_lb(arg_ls, arg_dic, channel, last_data_update):
    year = YEAR if "year" not in arg_dic else arg_dic["year"]
    leaderboard = LEADERBOARD if "leaderboard" not in arg_dic else arg_dic["leaderboard"]
    data = fetch_data(year, leaderboard, last_data_update, "force" in arg_dic)

    if len(arg_ls) == 0:
        day = str(datetime.now(TIMEZONE).day)
        table = get_table(day, data)
        if "detailed" in arg_dic:
            #lb d
            message = table_printer.print_full_lb_table(table, day, year, leaderboard, last_data_update)
        else:
            #lb
            message = table_printer.print_short_lb_table(table, day, year, leaderboard, last_data_update)
    else:
        day = arg_ls[0]
        if int(day) > int(datetime.now(TIMEZONE).day):
            await send_message("```I can't see into the future```", channel)
            return
        table = get_table(day, data, sorter="today_score")
        if "detailed" in arg_dic:
            #lb 1 d
            message = table_printer.print_full_lb_table_specific_day(table, day, year, leaderboard, last_data_update)
        else:
            #lb 1
            message = table_printer.print_short_lb_table_specific_day(table, day, year, leaderboard, last_data_update)

    await send_message(message, channel)

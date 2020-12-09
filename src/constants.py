import pytz
import os
from secret import SESSION_COOKIE, LEADERBOARD, DISCORD_CLIENT_ID, LID_1, LID_2, LID_3

YEAR = "2020"
DNF_STRING = "             DNF"
H24_STRING = "            >24h"
TIMEZONE = pytz.timezone("US/Eastern")
TEST_MODE = False
last_data_update = {}
SECONDS_IN_A_DAY = 86400
COOKIES = {
    'session': os.environ.get('ADVENT_COOKIE', SESSION_COOKIE)
}
DISCORD_CLIENT_ID = os.environ.get('ADVENT_BOT_ID', DISCORD_CLIENT_ID)
LEADERBOARD = os.environ.get('LEADERBOARD', LEADERBOARD)
LID_1 = os.environ.get('LID_1', LID_1)
LID_2 = os.environ.get('LID_2', LID_2)
LID_3 = os.environ.get('LID_3', LID_3)

####
test_data = ""

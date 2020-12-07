import pytz
import os
from secret import *

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

json_data = {}
data = []

####
test_data = ''

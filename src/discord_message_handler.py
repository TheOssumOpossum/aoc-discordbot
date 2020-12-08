from command_handler import handle_command_lb
from discord_api import send_message

last_data_update = {}

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
        await handle_command_lb(arg_ls, arg_dic, message.channel, last_data_update)
    elif channel_name == "advent-of-code-2020" and (command == "help"):
        f = open("messages/help.txt",'r')
        help_msg = f.read()
        f.close()
        await send_message(help_msg, message.channel)
    elif channel_name == "advent-of-code-2020" and (command == "ping"):
        await send_message("pong", message.channel)
    elif channel_name == "advent-of-code-2020" and (command == "repo"):
        f = open("messages/help.txt",'r')
        help_msg = f.read()
        f.close()
        await send_message("`https://github.com/TheOssumOpossum/discordbot`", message.channel)

def arg_parser(args):
    if isinstance(args,str):
        return ([args], {})
    keyed_params = {'--year','-y','--leaderboard','-l'}
    key_mapping = {'-y':'year', '--year':'year','--leaderboard':'leaderboard','-l':'leaderboard','--detailed':'detailed','-d':'detailed','-f':'force','--force':'force'}
    args_ls = []
    args_dic = {}
    key = False
    for arg in args:
        arg = str(arg)
        if key:
            args_dic[key] = arg
            key = False
        elif arg in keyed_params:
            key = key_mapping[arg]
        elif arg in key_mapping:
            args_dic[key_mapping[arg]] = ''
        else:
            args_ls.append(arg)
    return (args_ls, args_dic)

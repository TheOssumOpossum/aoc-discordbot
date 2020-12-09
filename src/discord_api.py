async def send_message(text, channel):
    if len(text) > 1950:
        page = 0
        last_num = 3
        yes_break = False
        while True:
            for i in range(last_num+1950,-1,-1):
                if i >= len(text):
                    yes_break = True
                    break
                if text[i] == '\n':
                    page += 1
                    await channel.send("```\n" + "page{0}".format(page) + text[last_num:i] + "\n```")
                    last_num = i
                    break
                if i == last_num:
                    print("returning early no new lines to splice")
                    yes_break = True
                    break
            if yes_break:
                page += 1
                await channel.send("```\n"+ "page{0}".format(page) + text[last_num:-4] + "\n```")
                break
    else:
        await channel.send(text)

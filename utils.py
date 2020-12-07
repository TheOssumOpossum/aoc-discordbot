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

from fuzzywuzzy import fuzz


# using Levenshtein algorithm
def recognize_cmd(cmd: str, check_list: list):
    rc = {'cmd': '', 'percent': 40}
    for c, v in check_list.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
    return rc
from fuzzywuzzy import fuzz
import json

with open("numbers.json", "r", encoding='utf-8') as file:
    numbers = json.load(file)

def sum_numbers(nums):
    wait_for = False
    summa = 0
    for i in range (len(nums)):
        if nums[i] in [20, 30, 40, 50, 60, 70, 80, 90]:
            summa = nums[i]
            wait_for = True
        elif not wait_for:
            return nums[i]
        else:
            if nums[i] in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                summa += nums[i]
            return summa
    return summa

def fetch_numbers(cmd: str):
    cmd = cmd.split(' ')
    record_nums = 'start'
    nums = []
    for i in range (len(cmd)):
        if record_nums == 'start' or record_nums == 'record':
            isNum = False
            for text, num in numbers.items():
                if cmd[i] == text:
                    nums.append(num)
                    isNum = True
                    record_nums = 'record'
                    break
            if not isNum and record_nums == 'record':
                record_nums = 'end'
    return nums

def get_number(cmd):
    nums = fetch_numbers(cmd)
    if not nums:
        return "None"
    return sum_numbers(nums)

# using Levenshtein algorithm
def levenshtein(cmd: str, check_list):
    likely_commands = []
    rc = {'cmd': '','arg': '', 'percent': 50}
    for c, v in check_list.items():
        if isinstance(v, dict):
            for c1, v1 in v.items():
                for x in v1:
                    vrt = fuzz.ratio(cmd, x)
                    if vrt > rc['percent']:
                        rc['cmd'] = c
                        rc['percent'] = vrt
                        rc['arg'] = c1
                        likely_commands.append(rc)
        else:
            for x in v:
                vrt = fuzz.ratio(cmd, x)
                if vrt > rc['percent']:
                    rc['cmd'] = c
                    rc['percent'] = vrt
                    likely_commands.append(rc)
    likely_commands.sort(key=lambda x: x['percent'], reverse=True)
    if not likely_commands:
        return rc
    return likely_commands[0]


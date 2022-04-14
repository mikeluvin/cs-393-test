import json
import sys


def parse_stdin():
    '''
    Return a list of parsed JSON objects read from STDIN.
    '''
    input_str = sys.stdin.read().strip()
    decoder = json.JSONDecoder()
    input_lst = []
    i = 0

    while i < len(input_str):
        try:   
            _json, consumed = decoder.raw_decode(input_str[i:])
            input_lst.append(_json)
            i += consumed
        except:
            i += 1

    return input_lst




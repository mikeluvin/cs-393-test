import json

def my_sort(input_lst):
    input_lst.sort(key=lambda obj: obj["content"])

    return input_lst
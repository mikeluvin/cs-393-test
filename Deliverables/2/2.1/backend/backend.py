import json

def my_sort(json_lst):
    input_lst = json.loads(json_lst)
    input_lst.sort(key=lambda obj: obj["content"])

    return json.dumps(input_lst)
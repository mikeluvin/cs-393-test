import json
from . import parse_stdin
from asst2 import my_sort

def main():
    input_lst = parse_stdin()
    # set of valid integers in the special object
    valid_range = set(range(1,25))
    special_objs = []
    result_lst = []

    for curr in input_lst:
        # check if curr is valid
        if not (isinstance(curr, dict) and len(curr) == 1 
                and type(curr.get("content", None)) == int
                and curr["content"] in valid_range):
            continue

        special_objs.append(curr)
        
        if len(special_objs) == 10:
            result_lst.append(my_sort(special_objs[:10]))
            special_objs = []

    print(json.dumps(result_lst))
        

if __name__ == "__main__":
    main()
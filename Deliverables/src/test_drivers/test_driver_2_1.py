import json
from . import parse_stdin
from asst2 import my_sort

def main():
    special_objs = parse_stdin()
    print(my_sort(json.dumps(special_objs[:10])))


if __name__ == "__main__":
    main()
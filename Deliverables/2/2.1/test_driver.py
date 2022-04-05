from backend.backend import my_sort
import json

def main():
    input_lst = []
    input_str = ""
    # see https://n8ta.com/python3/python/json/2021/04/09/how-to-parse-json-objects-from-stdin.html
    decoder = json.JSONDecoder()
    done = False
    while not done:
        input_str += input().lstrip()
        while len(input_str) > 0 and not done:
            try:
                parsed_json, consumed = decoder.raw_decode(input_str)
            except:
                break

            input_lst.append(parsed_json)
            # remove consumed bytes and strip whitespace
            input_str = input_str[consumed:].lstrip()
            if len(input_lst) >= 10:
                done = True
            

    print(my_sort(json.dumps(input_lst)))

if __name__ == "__main__":
    main()
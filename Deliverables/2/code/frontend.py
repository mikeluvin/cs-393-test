from backend import my_sort
import json

# check that dictionary instance
# size of dictionary is 1 and key is "content"
# check if in range of 1-24

def main():
    input_lst = []
    input_sublst = []
    input_str = ""
    # see https://n8ta.com/python3/python/json/2021/04/09/how-to-parse-json-objects-from-stdin.html
    decoder = json.JSONDecoder()
    done = False
    # set of valid integers in the special object
    valid_range = set(range(1,25))

    while True:
        try: 
            input_str += input().lstrip()
        except:
            break
        else: 
            while len(input_str) > 0 and not done:
                try:
                    _json, consumed = decoder.raw_decode(input_str)
                except:
                    break
                else:
                    # remove consumed bytes and strip whitespace
                    input_str = input_str[consumed:].lstrip()
                    # check if _json is valid
                    if not (isinstance(_json, dict) and len(_json) == 1 
                            and type(_json.get("content", None)) == int
                            and _json["content"] in valid_range):
                        continue

                    input_sublst.append(_json)
                    
                    if len(input_sublst) == 10:
                        input_lst.append(input_sublst)
                        input_sublst = []

    res_lst = []
    for lst in input_lst:
        res_lst.append(json.loads(my_sort(json.dumps(lst))))

    print(json.dumps(res_lst))

if __name__ == "__main__":
    main()
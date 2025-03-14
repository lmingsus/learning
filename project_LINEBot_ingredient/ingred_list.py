import os
import json
import random
import re
from collections import OrderedDict

if not os.path.exists('ingred_list.json'):
    print('Create ingred_list.json')
    with open('ingred_list.json', 'w') as f:
        json.dump({"ingredients":{}}, f)


def add_to_json(ingred_list):
    with open('ingred_list.json', 'r', encoding='utf-8') as f:
        ingred_json = json.load(f)

    # print(ingred_list)
    # ingred = "sodium fluoride (1440ppm F)"
    # ingred_list = ['AQUA', 'SORBITOL', 'HYDRATED SILICA', 'SODIUM LAURYL SULFATE', 'PROPYLENE GLYCOL', 'PEG-32', 'AROMA', 'TITANIUM DIOXIDE', 'SODIUM SACCHARIN', 'ALLANTOIN', 'CALCIUM GLYCEROPHOSPHATE']
    for ingred in ingred_list:
        ingred = ingred.split("(")[0].strip().upper()
        if ingred not in ingred_json["ingredients"] and is_valid_ingredient(ingred):
            ingred_json["ingredients"][ingred] = {}
    
    # 將 "ingredients" 中的元素按字母順序排序
    sorted_ingred = OrderedDict(sorted(ingred_json["ingredients"].items()))

    # 更新 JSON 結構
    ingred_json["ingredients"] = sorted_ingred

    with open('ingred_list.json', 'w', encoding='utf-8') as f:
        json.dump(ingred_json, f, ensure_ascii=False, indent=4)


def choose_empty_ingred():
    with open('ingred_list.json', 'r', encoding='utf-8') as f:
        ingred_json = json.load(f)
    
    empty_ingred_list = [ingred for ingred in ingred_json["ingredients"] if not len(ingred_json["ingredients"][ingred])]
    if not empty_ingred_list: # 如果沒有空的成分
        return None
    else:
        return random.choice(empty_ingred_list)
    


def add_ingred_contents(contents: str) -> bool:
    with open('ingred_list.json', 'r', encoding='utf-8') as f:
        ingred_json = json.load(f)
    
    # contents = "【 SODIUM LAURYL SULFATE 】\nzh:111 \nusage:222 \nsource:333 \nsafety:444 "
    ingredient = contents.split('】')[0].strip('【 ')
    zh = contents.split('zh:')[1].split('\n')[0].strip()
    usage = contents.split('usage:')[1].split('\n')[0].strip()
    source = contents.split('source:')[1].split('\n')[0].strip()
    safety = contents.split('safety:')[1].strip()

    if ingredient in ingred_json["ingredients"]:
        ingred_json["ingredients"][ingredient] = {"zh": zh, "usage": usage, "source": source, "safety": safety}
        with open('ingred_list.json', 'w', encoding='utf-8') as f:
            json.dump(ingred_json, f, ensure_ascii=False, indent=4)
        return True
    else:
        return False
    

def is_valid_ingredient(ingred: str) -> bool:
    return bool(re.match(r'^[A-Za-z0-9\s]*$', ingred))

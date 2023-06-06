from typing import Dict, List
import openai
import json
import pandas as pd
import precision_calculate as pc
import wikipedia
import re
from st_correction import do_st_corrections

wikipedia.set_lang("zh")
end_of_prompt = "\n\n###\n\n"
model = "babbage:ft-personal-2023-05-30-06-36-09"
output = open('output/train_doc5.jsonl', 'a', encoding='utf8')

def self_tt_special_table(text: str) -> str:
  res = text.replace("羣", "群")

  return res

def search_wiki(key_word) -> str:
    r = wikipedia.search(key_word, results=1)
    if len(r) == 0:
        return ""
    r = r[0]
    r = self_tt_special_table(do_st_corrections(r))
    return r

with open('data/unique_training_data.jsonl', 'r', encoding='utf8') as json_file:
    json_list = list(json_file)
    for json_str in json_list[1058:]:
        data = json.loads(json_str)
        id = data["id"]
        label = data["label"]
        prompt = data["claim"]
        evidence = data["evidence"]
        predicted_pages = []
        if label == "NOT ENOUGH INFO":
            result = openai.Completion.create(
                model=model,
                prompt=prompt+end_of_prompt,
                max_tokens=30,
                temperature=0,
                stop=["END"]
            )

            predicted_pages = result["choices"][0]["text"].strip().split("\n")
            wiki_search_results = []

            for possible_title in predicted_pages:
                wiki_search_results.append(search_wiki(possible_title))
                predicted_pages = list(set(wiki_search_results))
        
        else :
            for es in evidence:
                for e in es:
                    predicted_pages.append(e[2])
        
        json.dump({
            "id":id,
            "label":label,
            "claim":prompt,
            "evidence": evidence,
            "predicted_pages":list(set(predicted_pages))
            },
            output, ensure_ascii=False)
        output.write("\n")
        

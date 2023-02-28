import argparse
import os
import json
import nltk
nltk.download('punkt')
import pandas as pd
import numpy as np
from IPython.display import display

# difference between 2 sentences
def getTextDiff(txt1, txt2):
  tok1 = nltk.word_tokenize(txt1)
  tok2 = nltk.word_tokenize(txt2)

  max_len = max(len(tok1), len(tok2))
  diff = ''
  j=0
  for i in range(max_len):
    if len(tok1)>j and len(tok2)>i:
      if tok1[j] != tok2[i]:
        diff += tok2[i]
      else:
        j+=1
    else:
      if len(tok2)>i:
        diff += tok2[i]
  return diff

def loadSteretSet(file_path):
  with open(os.path.join(file_path), "r") as f:
    stereo_json = json.loads(f.read())

  print(stereo_json["data"]["intrasentence"][0])

  rows = []
  for i, bias_spec in enumerate(stereo_json["data"]["intrasentence"]):
    sentences = []
    labels = []
    att_terms = []
    for sentence_spec in bias_spec['sentences']:
      if sentence_spec['gold_label'] in  ['stereotype', 'anti-stereotype']:
        sentences.append(sentence_spec['sentence'])
        labels.append(sentence_spec["gold_label"])
        att_terms.append(getTextDiff(bias_spec["context"].replace("BLANK","").lower(), sentence_spec['sentence'].lower()))

    row = {"group": bias_spec["bias_type"],
            "group_term": bias_spec["target"],
            "template": bias_spec["context"].replace("BLANK", "[MASK]"),
            "att_term_1": att_terms[0],
            "att_term_2": att_terms[1],
            "label_1": labels[0],
            "label_2": labels[1]}
    
    rows.append(row)

  stereo_df = pd.DataFrame(rows)
  return stereo_df


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Process some arguments')
  parser.add_argument('--stereo_set_path', type=str, required=True, help="Source path to the json stereoset file")
  parser.add_argument('--out_path', type=str, required=True, help="Outpur directory to save csv sentence pairs into")

  args = parser.parse_args()
  print("Args:", args)

  # create headers for discard reason categories
  all_cats = list(range(10))[1:]
  all_cats.append('A')

  stereo_df = loadSteretSet(args.stereo_set_path) 
  stereo_df['discarded'] = ''
  stereo_df['discard_cats'] = ''
  for cat in all_cats:
    stereo_df[cat] = 0
  display(stereo_df.head(5))

  stereo_df.to_csv(os.path.join(args.out_path, os.path.basename(args.stereo_set_path).replace(".json",".csv")))
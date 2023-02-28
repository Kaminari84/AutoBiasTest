# AutoBiasTest
Repository for AutoBiasTest framework

If you have templates in paired format (check *gen_pairs_csv" for format) and you test Social Bias using Sterotype Score from [Nadeem'20](https://arxiv.org/abs/2004.09456) (stereotype/anti-stereotype pairs), you can start from **Step 3**

Starting from generations in JSON format in **./gen_json**
### Step 1: Turn JSON generations into CSV for editing discarded sentences
```
 python3 _1_gen2csv.py --source_path ./gen_json --out_path ./gen_csv
```

### Step 2: Turn CSV templates into stereotype/anti-stereotype pairs
```
 python3 _2_csv2pairs.py --source_path ./gen_csv --bias_spec_json bias_specs_with_glove_and_thesaurus.json --out_path ./gen_pairs_csv
```

### Step 3: Test Social Bias using Stereotype Score quantification metric from [Nadeem'20](https://arxiv.org/abs/2004.09456)
The tested model accepts paths from HuggingFace Transformer library, examples: *"bert-base-uncased", "bert-large-uncased", "gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl"*
```
 python3 _3_ss_test.py --gen_pairs_path ./ --bias_spec_json bias_specs_with_glove_and_thesaurus.json --tested_model  "bert-base-uncased" --out_path ./stereo_test      
```

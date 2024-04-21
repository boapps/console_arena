import requests
import jsonlines
from time import sleep
from tqdm import tqdm

with jsonlines.open('prompts.jsonl') as reader, jsonlines.open('puli_llumix_instruct.jsonl', mode='w') as writer:
    for obj in tqdm(reader):
        response = requests.post('https://puli.nytud.hu/api/forward', json={"path":"/demo/gpt/puli-llumix-instruct","temperature":0.4,"top_p":1,"top_k":50,"max_token":1500,"repetition_penalty":0.98,"diversity_penalty":None,"prompt":"","extra":None,"model":"puli-llumix-instruct","instruction":obj['input']})
        obj['output'] = response.json()['body']['text']
        writer.write(obj)
        sleep(5)

import requests
import jsonlines
from time import sleep
from tqdm import tqdm
from openai import OpenAI


client = OpenAI()

with jsonlines.open('prompts.jsonl') as reader, jsonlines.open('gpt_4_turbo.jsonl', mode='w') as writer:
    for obj in tqdm(reader):
        response = client.chat.completions.create(
          model="gpt-4-turbo-2024-04-09",
          messages=[
            {
              "role": "user",
              "content": obj['input']
            }
          ],
          temperature=0.9,
          max_tokens=1500,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        obj['output'] = response.choices[0].message.content
        writer.write(obj)
        sleep(5)

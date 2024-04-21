import os
import time
import argparse
import torch
import sampling
from rwkv_cpp import rwkv_cpp_shared_library, rwkv_cpp_model
from tokenizer_util import add_tokenizer_argument, get_tokenizer
from typing import List
import numpy as np
from tqdm import tqdm
import jsonlines

tokens_per_generation: int = 1000

# Sampling settings.
temperature: float = 0.8
top_p: float = 0.5


def parse_args():
    parser = argparse.ArgumentParser(description='Measure perplexity and per-token latency of an RWKV model on a given text file')
    parser.add_argument('model_path', help='Path to model checkpoint file', type=str)
    add_tokenizer_argument(parser)
    return parser.parse_args()

args = parse_args()

print('Loading model')
model: rwkv_cpp_model.RWKVModel = rwkv_cpp_model.RWKVModel(
    rwkv_cpp_shared_library.load_rwkv_shared_library(),
    args.model_path
)

print('Loading text')
text: str = 'Én vagyok a híres nagy fejű!'

tokenizer_decode, tokenizer_encode = get_tokenizer(args.tokenizer, model.n_vocab)

def generate(text):
    output_text = ''
    prompt: str = f"<|im_start|>system\nEgy segítőkész mesterséges intelligencia asszisztens vagy. Válaszold meg a kérdést legjobb tudásod szerint!<|im_end|>\n<|im_start|>user\n{text}\n<|im_start|>assistant"
    prompt_tokens: List[int] = tokenizer_encode(prompt)
    
    prompt_token_count: int = len(prompt_tokens)
    print(f'{prompt_token_count} tokens in prompt')
    
    init_logits, init_state = model.eval_sequence_in_chunks(prompt_tokens, None, None, None, use_numpy=True)
    logits, state = init_logits.copy(), init_state.copy()

    for i in range(tokens_per_generation):
        token: int = sampling.sample_logits(logits, temperature, top_p)
        if token == 0:
            break

        print(tokenizer_decode([token]), end='', flush=True)
        output_text += tokenizer_decode([token])
        if '<|im_end|>' in output_text:
            output_text = output_text.replace('<|im_end|>', '')
            break

        logits, state = model.eval(token, state, state, logits, use_numpy=True)
    return output_text

with jsonlines.open('prompts.jsonl') as reader, jsonlines.open('szm_rwkv5_3B.jsonl', mode='w') as writer:
    for obj in tqdm(reader):
        obj['output'] = generate(obj['input'])
        writer.write(obj)


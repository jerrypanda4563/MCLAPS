import spacy
from typing import List


tokenizer = spacy.load("en_core_web_sm")
def tokenize_string(input_string) -> List[str]:
    tokens = [token.text for token in tokenizer(input_string)]
    return tokens

def chunk_string(input_string: str) -> List[str]:
    tokenized_string = tokenize_string(input_string)
    chunks=[]
    current_chunk = []

    for token in tokenized_string:
        if len(current_chunk) < 10:
            current_chunk.append(token)
        else:
            current_string_chunk = " ".join(current_chunk)
            chunks.append(current_string_chunk)
            current_chunk = [token]  # start a new chunk with the current token

    # Add the last chunk if it's not empty
    if current_chunk:
        current_string_chunk = " ".join(current_chunk)
        chunks.append(current_string_chunk)

    return chunks

def chunk_string_large(input_string: str) -> List[str]:
    tokenized_string = tokenize_string(input_string)
    chunks=[]
    current_chunk = []

    for token in tokenized_string:
        if len(current_chunk) < 100:
            current_chunk.append(token)
        else:
            current_string_chunk = " ".join(current_chunk)
            chunks.append(current_string_chunk)
            current_chunk = [token]  # start a new chunk with the current token

    # Add the last chunk if it's not empty
    if current_chunk:
        current_string_chunk = " ".join(current_chunk)
        chunks.append(current_string_chunk)

    return chunks





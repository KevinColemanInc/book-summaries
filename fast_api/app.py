from fastapi import FastAPI
import numpy as np
import faiss                   # make faiss available
from transformers import AutoTokenizer, TFAutoModel

model_ckpt = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
model = TFAutoModel.from_pretrained(model_ckpt, from_pt=True)

d = 768                           # dimension


index = faiss.IndexFlatL2(d)   # build the index
print(index.is_trained)
print(index.ntotal)

K = 10

vector_id_to_summary = {} # stores id to chapter

def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]

app = FastAPI()
def get_embeddings(text_list):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="tf"
    )
    encoded_input = {k: v for k, v in encoded_input.items()}
    print('encoded_input', encoded_input)
    model_output = model(**encoded_input)
    res = cls_pooling(model_output)
    return { "vectors": (res.numpy().tolist())}

@app.get("/query")
async def query(q: str, chapter: int):

    # create search embedding
    search_embedding = get_embeddings([q])

    # search vector db
    _, I = index.search([search_embedding], 20) # 
    I = I[0]

    # filter vector db results
    results = []
    for i in I:
        if I[i][0] not in vector_id_to_summary:
            summary = vector_id_to_summary[xb[i][0]]
            if summary["chapter"] <= chapter:
                results.append(summary)
    return results
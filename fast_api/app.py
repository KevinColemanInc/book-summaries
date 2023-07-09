from fastapi import FastAPI
import numpy as np
import csv
import os
import faiss                   # make faiss available
from transformers import AutoTokenizer, TFAutoModel
from fastapi.middleware.cors import CORSMiddleware
from pymilvus import MilvusClient

model_ckpt = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
model = TFAutoModel.from_pretrained(model_ckpt, from_pt=True)

d = 768                           # dimension

index = faiss.IndexFlatL2(d)   # build the index
index = faiss.IndexIDMap(index)

# Milvus
endpoint = 'https://in03-a8addf495e0d26b.api.gcp-us-west1.zillizcloud.com'
token = os.environ.get('zillizcloud_token')
collection_name = 'booksummaries'

client = MilvusClient(
    uri=endpoint, # Cluster endpoint obtained from the console
    token=token
)

K = 10

vector_id_to_summary = {} # stores id to chapter

def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_embeddings(text_list):
    encoded_input = tokenizer(
        text_list, padding=True, truncation=True, return_tensors="tf"
    )
    encoded_input = {k: v for k, v in encoded_input.items()}
    model_output = model(**encoded_input)
    res = cls_pooling(model_output)
    return res.numpy().tolist()[0]

def index_summaries(faiss_index):
    path = '../books/sherlock_holmes'

    counter = 0
    #walk summary files csv
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv'):
                with open(os.path.join(root, file), 'r') as f:
                    reader = csv.reader(f)
                    for idx, row in enumerate(reader):
                        if idx == 0:
                            continue
                        vector =  get_embeddings([row[5]])
                        faiss_index.add_with_ids(np.array(vector).astype("float32").reshape(1, d), np.array([counter]))
                        vector_id_to_summary[counter] = {"chapter": int(row[1]), "summary": row[5], "chunk_list_id": row[2], "vector": vector}
                        # res = client.insert(
                        #     collection_name=collection_name,
                        #     data={"chapter": int(row[1]), "summary": row[5], "data": vector}
                        # )

                        # print(res)
                        counter += 1


index_summaries(index)

@app.get("/query")
async def query(q: str, chapter: int):

    # create search embedding
    search_embedding = get_embeddings([q])

    # search vector db
    _, I = index.search(np.array([search_embedding]), 100) # 
    I = I[0]

    # filter vector db results
    results = []
    for i in I:
        if i in vector_id_to_summary:
            summary = vector_id_to_summary[i]
            if summary["chapter"] <= chapter:
                results.append(summary)
    return results

@app.get("/milvus")
async def milvus(q: str, chapter: int):

    # create search embedding
    search_embedding = get_embeddings([q])

    # search vector db
    res = client.search(
        collection_name=collection_name,
        data=[search_embedding],
        limit=200,
        output_fields=["summary", "vector", "chapter"]
    )
    # filter vector db results
    results = []
    for result in res:
        print('result', len(result))
        entity = result[0]["entity"]
        if entity["chapter"] <= chapter:
            results.append({"summary": entity["summary"], "chapter": entity["chapter"]})
    return results
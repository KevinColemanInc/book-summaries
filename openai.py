import requests
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import csv

column_names_csv = ["book_name", "chapter_number", "chunk_list_id", "original_text_chunk", "summary_chunk"]
complete_summary = ""
text_splitter = CharacterTextSplitter()


with open("/Users/rahul.khandalkar/Documents/Personal/book-summaries/books/sherlock_holmes/chapter_13.txt") as f:
    chapters_sentence = f.read()
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 3000,
    chunk_overlap  = 50,
    length_function = len,
)
texts = text_splitter.split_text(chapters_sentence)
res = []
for sub in texts:
    res.append(sub.replace("\n", ""))
# print(res)
start_list = 0
end_list = 1
print(len(res))
while len(res)+1 != end_list:
    res_initial = res[start_list:end_list]

    original_text_chunk_char_count = min(len(entry) for entry in res_initial)
    # Print the smallest character count
    print("character_count")
    print(original_text_chunk_char_count)

    # print(res_intial)
    # print(len(res_intial))

    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'model': 'gpt-4',
        'messages': [
            {
                'role': 'user',
                'content': f"summarize+ {res_initial}",
            },
        ],
    }

    response = requests.post('http://3.88.181.187:8080/v1/', headers=headers, json=json_data)

    print(response.json())
    content = response.json()['choices'][0]['message']['content']
    print(content)
    summary_text_chunk_char_count = len(content)
    # Print the smallest character count
    print("summary_text_chunk_char_count")
    print(summary_text_chunk_char_count)

    complete_summary = complete_summary + content

    print("=================================================================================")
    print("complete_summary")
    print(complete_summary)

    row_to_append = ["Sherlock Homes","13",end_list,res_initial,original_text_chunk_char_count,content,summary_text_chunk_char_count]
    with open("/Users/rahul.khandalkar/Documents/Personal/book-summaries/books/sherlock_holmes/chapter_13_summary.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row_to_append)
    start_list+=1
    end_list+=1

    

# while end_list > len(res_intial):
#     res = res[start_list:end_list]
#     smallest_character_count = min(len(entry) for entry in res)
#     # Print the smallest character count
#     print("smallest_character_count")
#     print(smallest_character_count)

#     largest_character_count = max(len(entry) for entry in res)
#     print("largest_character_count")
#     print(largest_character_count)

#     total_character_count = sum(len(entry) for entry in res)
#     print("total_character_count")
#     print(total_character_count)

#     start_list = start_list + 31
#     end_list = end_list + 31


# print(texts[1])
# text_splitter.split_text(state_of_the_union)[:2]
# docs = [Document(page_content=t) for t in texts[:3]]



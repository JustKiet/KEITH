import requests
import os
import json
import time

#files = os.listdir("output/documents/202501")
#
#documents = []
#for file in files:
#    with open(f"output/documents/202501/{file}", "r") as f:
#        data = json.load(f)
#        documents.append(data)
#
#if not os.path.exists("output/document_chunks"):
#    os.makedirs("output/document_chunks")
#
#if not os.path.exists("output/documents_json"):
#    os.makedirs("output/documents_json")
#
#if not os.path.exists("output/vectorized_documents"):
#    os.makedirs("output/vectorized_documents")
#
#with open(f"output/documents_json/202501.json", "w") as f:
#    json.dump(documents, f, ensure_ascii=False, indent=4)
#
#
#chunked_documents = requests.post(url="http://0.0.0.0:6091/api/chunking/recursive_chunk_pdfs", 
#                                  json={"documents": documents, "chunk_size": 10000, "separator": "."})
#
#if chunked_documents.status_code != 200:
#    print(chunked_documents.json())
#
#with open(f"output/document_chunks/202501.json", "w") as f:
#    json.dump(chunked_documents.json(), f, ensure_ascii=False, indent=4)
#
##vectorized_documents = requests.post(url="http://0.0.0.0:6092/api/pdf/vectorize",
#                                     json=chunked_documents.json())
#
#if vectorized_documents.status_code != 200:
#    print(vectorized_documents.json())
#
#with open(f"output/vectorized_documents/202501.json", "w") as f:
#    json.dump(vectorized_documents.json(), f, ensure_ascii=False, indent=4)

#with open(f"output/vectorized_documents/202501.json", "r") as f:
#    vectorized_documents = json.load(f)
#
#insert_response = requests.post(url="http://0.0.0.0:6093/api/milvus/insert", json=vectorized_documents)
#
#print(insert_response.json())

vectorize_query = requests.post(url="http://0.0.0.0:6092/api/query/vectorize", params={"query": "What is the capital of France?"})

query_response = requests.post(url="http://0.0.0.0:6093/api/milvus/query_with_reranking", json={"query_vector":vectorize_query.json()["embedding"], "top_k": 5})

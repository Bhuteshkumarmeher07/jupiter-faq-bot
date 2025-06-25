import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load cleaned FAQs
with open("cleaned_faqs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

questions = [item["question"] for item in data]
model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight and fast

# Generate embeddings
embeddings = model.encode(questions, convert_to_numpy=True)

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

def search_faq(query, top_k=3):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append(data[idx])
    return results




# Test the search
query = "how to update my KYC"
results = search_faq(query)

print("\nTop Results:\n")
for i, r in enumerate(results, 1):
    print(f"{i}. Q: {r['question']}\n   A: {r['answer'][:200]}...\n")


#----------------------------------------------------------------------------
from rephrase_with_mistral import rephrase_with_mistral
from semantic_search import search_faq

api_key = "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"  # <-- Paste your actual API key here

query = "how do I update my KYC?"
top_faq = search_faq(query)[0]

print("🔎 FAQ Retrieved:")
print(top_faq['question'])
print(top_faq['answer'])

# Now rephrase
print("\n💬 Rephrased Answer:")
#print(rephrase_with_mistral(top_faq['question'], top_faq['answer'], api_key))
print(rephrase_with_mistral(query, [top_faq], api_key))  # use a list of one FAQ


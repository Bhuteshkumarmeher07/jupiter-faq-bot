import json
import re

# Load raw scraped data
with open("jupiter_help_faqs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned_data = []

for item in data:
    q = item["question"].strip()
    a = item["answer"].strip()

    # Skip if answer is too short or auto-tagged
    if len(a) < 15 or "@Shawnpinto" in a or "@Nikhil_Godbole" in a:
        continue

    # Remove line breaks and extra spaces
    a = re.sub(r"\s+", " ", a)
    q = re.sub(r"\s+", " ", q)

    cleaned_data.append({
        "question": q,
        "answer": a,
        "url": item["url"]
    })

# Save cleaned output
with open("cleaned_faqs.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

print(f"✅ Cleaned and saved {len(cleaned_data)} entries to cleaned_faqs.json")

import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import time

BASE_URL = "https://community.jupiter.money/c/help/27"
CATEGORY_URL = f"{BASE_URL}/c/help/27.json"  # JSON endpoint of the Help category

def fetch_topic_urls():
    res = requests.get(CATEGORY_URL)
    data = res.json()
    topic_urls = [f"{BASE_URL}/t/{topic['slug']}/{topic['id']}" for topic in data['topic_list']['topics']]
    return topic_urls

def scrape_topic(url):
    topic_id = url.split("/")[-1]
    topic_json_url = f"https://community.jupiter.money/t/{topic_id}.json"
    
    res = requests.get(topic_json_url)
    data = res.json()

    question = data['title']
    posts = data['post_stream']['posts']

    if not posts or len(posts) == 0:
        return None

    # First post = original question or context
    first_post = posts[0]['cooked']
    # Next post = usually the first answer
    if len(posts) > 1:
        answer_post = posts[1]['cooked']
    else:
        answer_post = first_post

    # Remove HTML tags
    from bs4 import BeautifulSoup
    q_clean = BeautifulSoup(first_post, "html.parser").get_text()
    a_clean = BeautifulSoup(answer_post, "html.parser").get_text()

    return {
        "url": url,
        "question": question,
        "context": q_clean.strip(),
        "answer": a_clean.strip()
    }


def main():
    topic_urls = fetch_topic_urls()
    print(f"Found {len(topic_urls)} topics.")

    faqs = []
    for url in tqdm(topic_urls):
        try:
            faq = scrape_topic(url)
            if faq:
                faqs.append(faq)
            time.sleep(1)  # Avoid hitting rate limits
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # Save as JSON
    with open("jupiter_help_faqs.json", "w", encoding="utf-8") as f:
        json.dump(faqs, f, indent=2, ensure_ascii=False)

    print("✅ Scraping complete. Saved to jupiter_help_faqs.json")

if __name__ == "__main__":
    main()

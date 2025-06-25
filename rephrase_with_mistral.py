import requests
import json

def rephrase_with_mistral(query, top_faqs, api_key):
    faq_block = "\n\n".join(
        [f"{i+1}. Q: {faq['question']}\n   A: {faq['answer']}" for i, faq in enumerate(top_faqs)]
    )

    prompt = f"""
You are an intelligent FAQ assistant for a digital bank.

A user asked this question:
\"{query}\"

Below are 3 FAQ entries retrieved as possibly relevant:

{faq_block}

Instructions:
1. Read all 3 FAQs carefully.
2. Decide which FAQ (if any) actually answers the user's question.
3. If **none** are truly relevant, say: "Sorry, I couldn’t find a relevant answer. Please contact support."
4. If one FAQ is relevant, use it to write a helpful, friendly, and clear response.
5. Do not guess or hallucinate. Be honest if nothing fits.
6. ✅ Do NOT explain your steps or say things like "Here's a suitable response." Just write the final response only.
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://yourapp.com",
        "X-Title": "Jupiter FAQ Bot"
    }

    data = {
        "model": "mistralai/mistral-small-3.2-24b-instruct-2506:free",
        "messages": [
            {"role": "system", "content": "You are a helpful and honest banking assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        result = response.json()

        token_usage = None
        if "usage" in result:
            token_usage = {
                "prompt": result["usage"].get("prompt_tokens", 0),
                "completion": result["usage"].get("completion_tokens", 0),
                "total": result["usage"].get("total_tokens", 0),
            }

        if "choices" in result:
            raw_answer = result["choices"][0]["message"]["content"]

            if "sorry" in raw_answer.lower() or "couldn't find" in raw_answer.lower():
                raw_answer += (
                    "\n\n💡 Still need help?\n"
                    "For faster response, customers can **call Jupiter customer care at +91 8655055086** "
                    "(9 AM to 7 PM on weekdays) or **chat with executives in the app**.\n\n"
                    "You can also lodge a complaint via the Jupiter App or **email support@jupiter.money** from your registered email ID.\n"
                    "For general info, visit the [Jupiter Help Center](https://support.jupiter.money)."
                )

            return raw_answer, token_usage

        elif "error" in result:
            return f"❌ API Error: {result['error']['message']}", token_usage
        else:
            return "❌ Unknown error occurred during rephrasing.", token_usage

    except Exception as e:
        return f"❌ Request failed: {str(e)}", None

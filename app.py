import streamlit as st
import re
import csv
from datetime import datetime
from semantic_search import search_faq
from rephrase_with_mistral import rephrase_with_mistral
from langdetect import detect
from googletrans import Translator

st.set_page_config(page_title="Jupiter FAQ Bot", layout="centered")
st.title("🤖 Jupiter Help Center FAQ Bot")
st.write("Ask anything related to Jupiter features, KYC, debit cards, payments, or support.")

api_key = st.text_input("🔑 Enter your OpenRouter API Key", type="password")
query = st.text_input("💬 Your Question")

st.session_state.setdefault("last_answer", None)
st.session_state.setdefault("token_usage", None)
st.session_state.setdefault("top_faqs", None)

def strip_personal_names(text):
    return re.sub(r"(Hi|Hello)[\s,]+[A-Z][a-z]+!?[,]?", "Hello", text)

def log_feedback(query, answer, helpful, comment):
    with open("feedback_log.csv", mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), query, answer, helpful, comment])

def translate_to_english(text):
    try:
        lang = detect(text)
        if lang != "en":
            translator = Translator()
            return translator.translate(text, dest="en").text
    except:
        pass
    return text

if st.button("Get Answer", key="get_answer_button"):
    if not api_key:
        st.warning("⚠️ Please enter your OpenRouter API key.")
    elif not query:
        st.warning("⚠️ Please enter your question.")
    else:
        translated_query = translate_to_english(query)

        with st.spinner("🔍 Searching best match..."):
            top_faqs = search_faq(translated_query, top_k=3)
            if not top_faqs:
                st.error("❌ No matching FAQs found.")
            else:
                for faq in top_faqs:
                    faq['answer'] = strip_personal_names(faq['answer'])
                    faq['question'] = strip_personal_names(faq['question'])

                selected_faq = top_faqs[0]
                st.subheader("🔎 Most Relevant FAQ")
                st.markdown(f"**Q:** {selected_faq['question']}")
                st.markdown(f"**Original A:** {selected_faq['answer']}")

                with st.spinner("✍️ Rephrasing with Mistral 3.2 24B..."):
                    friendly_answer, token_usage = rephrase_with_mistral(translated_query, top_faqs, api_key)

                st.session_state.last_answer = friendly_answer
                st.session_state.token_usage = token_usage
                st.session_state.top_faqs = top_faqs

if st.session_state.last_answer:
    st.subheader("💡 Rephrased Answer")
    st.success(st.session_state.last_answer)

    if st.session_state.token_usage:
        t = st.session_state.token_usage
        st.markdown(f"🧮 **Token usage:** Prompt: {t['prompt']} | Completion: {t['completion']} | Total: {t['total']}")

    st.subheader("📝 Feedback")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Yes", key="feedback_yes"):
            log_feedback(query, st.session_state.last_answer, "Yes", "")
            st.success("✅ Thanks for your feedback!")
    with col2:
        if st.button("👎 No", key="feedback_no"):
            comment = st.text_input("What could be improved?", key="comment_input")
            if comment:
                log_feedback(query, st.session_state.last_answer, "No", comment)
                st.success("✅ Feedback submitted. Thanks!")

    with st.expander("📚 See Top 3 Matched FAQs"):
        for i, faq in enumerate(st.session_state.top_faqs):
            st.markdown(f"**{i+1}.** {faq['question']}\n> {faq['answer'][:200]}...")

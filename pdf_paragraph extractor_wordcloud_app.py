import streamlit as st
import pdfplumber
import nltk
import re
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud

# Download NLTK resources
nltk.download("punkt")
nltk.download("stopwords")

# Title
st.title("🔍 PDF Paragraph Extractor + Word Cloud Generator")
st.write("Upload a PDF and enter multiple keywords to extract relevant paragraphs and generate a word cloud.")

# Upload PDF
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# Keyword input
keywords_input = st.text_input("Enter keywords (comma-separated)", "")

# Process only if both PDF and keywords provided
if uploaded_file and keywords_input.strip():

    keywords = [k.strip().lower() for k in keywords_input.split(",") if k.strip()]
    st.write(f"### 🔎 Searching for paragraphs containing ALL keywords: {keywords}")

    # Read PDF using pdfplumber
    full_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    if not full_text.strip():
        st.error("No extractable text found in the PDF.")
        st.stop()

    paragraphs = [p.strip() for p in full_text.split("\n\n") if len(p.strip()) > 20]

    matched_paragraphs = []
    for para in paragraphs:
        low_para = para.lower()
        if all(k in low_para for k in keywords):
            matched_paragraphs.append(para)

    if matched_paragraphs:
        st.subheader("📄 Extracted Paragraphs Containing All Keywords")
        for p in matched_paragraphs:
            st.write("- " + p)
    else:
        st.warning("No paragraphs matched all keywords.")
        st.stop()

    combined_text = " ".join(matched_paragraphs)

    clean = re.sub(r"[^a-zA-Z\s]", " ", combined_text.lower())
    clean = re.sub(r"\s+", " ", clean)

    tokens = word_tokenize(clean, preserve_line=True)

    stop_words = set(stopwords.words("english"))
    words = [w for w in tokens if w not in stop_words and len(w) > 2]

    if len(words) == 0:
        st.error("No valid words found to generate a word cloud.")
        st.stop()

    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color="white",
        stopwords=stop_words,
        colormap="viridis",
        max_words=200,
    ).generate(" ".join(words))

    st.subheader("☁ Word Cloud of Extracted Paragraphs")
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

else:
    st.info("Please upload a PDF and enter keywords to begin.")

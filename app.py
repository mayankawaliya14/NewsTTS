import streamlit as st
import requests
import subprocess
import time
import os

st.title("📰 News Sentiment and Hindi TTS App")

company = st.text_input("Enter Company Name")

if st.button("Analyze"):
    with st.spinner("Fetching news..."):
        res = requests.get(f"http://127.0.0.1:8000/news?company={company}")
        data = res.json()

    st.subheader(f"📊 Final Sentiment: {data['Final Sentiment Analysis']}")

    st.subheader("🗞️ Articles")
    for i, article in enumerate(data["Articles"], 1):
        st.markdown(f"**{i}. {article['Title']}**")
        st.write(f"Summary: {article['Summary']}")
        st.write(f"Sentiment: `{article['Sentiment']}`")
        st.write(f"Topics: {', '.join(article['Topics'])}")
        st.markdown("---")

    st.subheader("📈 Comparative Analysis")
    st.write(data["Comparative Sentiment Score"])

    st.subheader("🔊 Listen to Summary in Hindi")
    st.audio(data["Audio"])

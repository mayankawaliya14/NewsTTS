import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd
from gtts import gTTS
from googletrans import Translator
import re



def get_news_articles(company_name):
    search_url = f"https://news.google.com/search?q={company_name}&hl=en-IN&gl=IN&ceid=IN:en"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []

    for item in soup.find_all("article")[:10]:
        title_tag = item.find("a", class_="JtKRv")
        title = title_tag.text if title_tag else None

        link = title_tag['href'] if title_tag and title_tag.has_attr('href') else None
        if link and link.startswith("./"):
            link = "https://news.google.com" + link[1:]

        source_tag = item.find("div", class_="vr1PYe")
        source = source_tag.text if source_tag else "Unknown Source"

        time_tag = item.find("time")
        time = time_tag.text if time_tag else "Unknown Time"

        if title and link:
            articles.append({
                "title": title,
                "link": link,
                "source": source,
                "time": time,
                "summary": title  
            })

    return articles

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"
    

def comparative_analysis(articles):
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    comparisons = []
    
    for article in articles:
        sentiment_counts[article["sentiment"]] += 1

    if len(articles) > 1:
        for i in range(len(articles) - 1):
            comparison = {
                "Comparison": f"{articles[i]['title']} vs {articles[i+1]['title']}",
                "Impact": f"{articles[i]['sentiment']} vs {articles[i+1]['sentiment']}"
            }
            comparisons.append(comparison)

    return {
        "Sentiment Distribution": sentiment_counts,
        "Comparisons": comparisons
    }

def generate_hindi_tts(articles, filename="output.mp3"):
    translator = Translator()

    if not articles:
        text = "कोई समाचार उपलब्ध नहीं है।"
    else:
        text = "कंपनी से जुड़ी 10 ताज़ा खबरें:\n"
        for i, article in enumerate(articles):
            try:
                translated = translator.translate(article['title'], dest='hi').text
                text += f"समाचार {i+1}: {translated}. "
            except Exception as e:
                print(f"[ERROR] Translation failed for article {i+1}: {e}")
                text += f"समाचार {i+1}: {article['title']}. "

    try:
        tts = gTTS(text=text, lang="hi")
        tts.save(filename)
    except Exception as e:
        print(f"[ERROR] TTS generation failed: {e}")
        return None

    return filename

def extract_topics(text):
    if not text:
        return []

    words = re.findall(r'\b[A-Z][a-zA-Z]+\b', text)
    keywords = list(set(words))
    return keywords[:4]  
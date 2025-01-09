import requests
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from groq import Groq
from transformers import pipeline, AutoTokenizer
from eventregistry import *

# API Configuration
GROQ_API_KEY = "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"
EVENT_REGISTRY_API_KEY = "3213d8d5-4bfd-4d54-9e99-420f6aea559e"

# Model names
SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"

# Initialize Groq client
def initialize_groq():
    return Groq(api_key=GROQ_API_KEY)

def initialize_sentiment_analyzer():
    tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL)
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=SENTIMENT_MODEL,
        tokenizer=tokenizer
    )
    return sentiment_pipeline, tokenizer

def truncate_for_model(text, tokenizer, max_length=512):
    tokens = tokenizer.encode(text, truncation=False)
    if len(tokens) > max_length:
        tokens = tokens[:max_length-1] + [tokenizer.sep_token_id]
        text = tokenizer.decode(tokens, skip_special_tokens=True)
    return text

def truncate_for_llama(text, max_length=900):
    words = text.split()
    if len(words) > max_length:
        return ' '.join(words[:max_length]) + "..."
    return text

# Function to fetch news data from Event Registry
def fetch_news(max_items=100):
    try:
        er = EventRegistry(apiKey=EVENT_REGISTRY_API_KEY)

        q = QueryArticlesIter(
            keywords=QueryItems.OR([
                "Sugar", "Sugarcane", "Sugar Refining", 
                "Food Prices", "Sweeteners", "Sugar Supply Chain"
            ]),
            dateStart=(dt.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            dateEnd=dt.now().strftime('%Y-%m-%d'),
            dataType=["news", "blog"],
            lang="eng"
        )

        articles = []
        for article in q.execQuery(er, sortBy="date", maxItems=max_items):
            articles.append(article)

        return {"articles": {"results": articles}}
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

# Risk analysis with Groq LLaMa
def analyze_risk_with_llama(content, client):
    try:
        truncated_content = truncate_for_llama(content)

        prompt = f"""Analyze the following news article for Sugar supply chain risks.

        Consider these specific factors:
        1. Agricultural Risks
            - Weather conditions affecting sugarcane/sugar beet crops (e.g., drought, floods, pests)
            - Dependency on specific regions for sugar production
            - Long growth cycles leading to supply delays

        2. Manufacturing Risks
            - Refining capacity limitations
            - Contamination risks during processing
            - Delays in refining or transportation due to technical issues
            
        3. Geographic Risks
            - Heavy reliance on specific agricultural hubs
            - Political instability or natural disasters affecting key regions
            - Transportation challenges in moving raw and refined sugar
            
        4. Economic and Political Risks
            - Price fluctuations in global sugar markets
            - Trade restrictions or tariffs
            - Currency exchange rates impacting imports/exports

        5. Industry Impact
            - Shortages affecting the food and beverage industries
            - Rising costs for consumers
            - Reputational risks for companies due to supply chain disruptions
            
        6. Mitigation Strategies
            - Diversifying sourcing regions for sugarcane and sugar beets
            - Investment in modern refining technologies
            - Strategic stockpiling and predictive analytics in supply chains

        Article: {truncated_content}

        Provide a structured analysis of the identified risks and their potential impact on the Sugar supply chain."""

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False
        )

        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error with Groq LLaMa: {e}")
        return "Error in risk analysis"

# Sentiment analysis with proper truncation
def analyze_sentiment_with_model(content, sentiment_pipeline, tokenizer):
    try:
        truncated_content = truncate_for_model(content, tokenizer)
        result = sentiment_pipeline(truncated_content)[0]

        return {
            "label": result["label"],
            "score": float(result["score"]),
            "analysis": f"Sentiment: {result['label']} (confidence: {result['score']:.2f})"
        }
    except Exception as e:
        print(f"Error with sentiment analysis: {e}")
        return {
            "label": "ERROR",
            "score": 0.0,
            "analysis": "Error in sentiment analysis"
        }

# Aggregate data into structured format
def aggregate_data(news_data):
    try:
        structured_data = []
        for article in news_data.get('articles', {}).get('results', []):
            structured_data.append({
                "source": article.get('source', {}).get('title', ''),
                "title": article.get('title', ''),
                "description": article.get('body', ''),
                "content": article.get('body', ''),
                "published_at": article.get('dateTime', '')
            })
        return pd.DataFrame(structured_data)
    except Exception as e:
        print(f"Error structuring data: {e}")
        return None

# Main pipeline
def main():
    groq_client = initialize_groq()
    sentiment_pipeline, tokenizer = initialize_sentiment_analyzer()

    news_data = fetch_news(max_items=10)
    if not news_data:
        return

    structured_data = aggregate_data(news_data)
    if structured_data is None or structured_data.empty:
        print("No data to analyze")
        return

    results = []
    for idx, row in structured_data.iterrows():
        print(f"\nAnalyzing article {idx + 1}/{len(structured_data)}: {row['title']}")

        risk_analysis = analyze_risk_with_llama(row['content'], groq_client)
        sentiment_analysis = analyze_sentiment_with_model(row['content'], sentiment_pipeline, tokenizer)

        results.append({
            'Title': row['title'],
            'Source': row['source'],
            'Published At': row['published_at'],
            'Sentiment': sentiment_analysis['label'],
            'Sentiment Score': sentiment_analysis['score'],
            'Sentiment Analysis': sentiment_analysis['analysis'],
            'Risk Analysis': risk_analysis
        })

    results_df = pd.DataFrame(results)
    results_df.to_csv("Sugar_Risk_and_Sentiment_Results.csv", index=False, encoding='utf-8')

    print("Analysis saved to Sugar_Risk_and_Sentiment_Results.csv")

if __name__ == "__main__":
    main()

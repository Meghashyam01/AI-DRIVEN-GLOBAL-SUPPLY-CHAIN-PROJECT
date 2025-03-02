import requests
import pandas as pd

# API key and base URL
api_key = "6ddbb12e635247a7b0d17dcc31a91346"
base_url = "https://newsapi.org/v2/everything"

# List of keywords to search
keywords = [
    "supply chain disruption",
    "Sugar",
    "Sugarcane",
    "Sugar Refining",
    "Sugar Supply Chain"
]

# Initialize an empty list to store all articles
all_articles = []

# Loop through each keyword and make API requests
for keyword in keywords:
    params = {
        'q': keyword,  # Search query
        'language': 'en',  # Language filter
        'pageSize': 100,  # Maximum number of results
        'apiKey': api_key  # API key
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        print(f"API request successful for keyword: '{keyword}'")
        data = response.json()

        # Check if articles are present
        if 'articles' in data and data['articles']:
            articles = data['articles']
            # Append articles to the all_articles list
            all_articles.extend(articles)
        else:
            print(f"No articles found for keyword: '{keyword}'")
    else:
        print(f"Error for keyword '{keyword}': {response.status_code} - {response.text}")

# Check if any articles were collected
if all_articles:
    # Create a DataFrame from all collected articles
    news_df = pd.DataFrame([{
        'Title': article.get('title'),
        'Description': article.get('description'),
        'Source': article['source'].get('name'),
        'Published Date': article.get('publishedAt'),
        'URL': article.get('url')
    } for article in all_articles])

    print("\nCollected News Articles:")
    print(news_df)

    # Save as CSV
    news_df.to_csv("Supply_Chain_Impact_News.csv", index=False)

    print("\nTop News Titles:")
    for idx, title in enumerate(news_df['Title'], start=1):
        print(f"{idx}. {title}")
else:
    print("No articles found for any keywords.")
import requests
import pandas as pd

api_key = "6ddbb12e635247a7b0d17dcc31a91346"
base_url = "https://newsapi.org/v2/everything"
params = {
    'q': 'supply chain disruption',  # Search query
    'language': 'en',  # Language filter
    'pageSize': 10,  # Maximum number of results
    'apiKey': api_key  # API key
}

# Make the API request
response = requests.get(base_url, params=params)

if response.status_code == 200:
    print("API request successful!")
    data = response.json()

    # Check if articles are present
    if 'articles' in data and data['articles']:
        articles = data['articles']
        news_df = pd.DataFrame([{
            'Title': article.get('title'),
            'Description': article.get('description'),
            'Source': article['source'].get('name'),
            'Published Date': article.get('publishedAt'),
            'URL': article.get('url')
        } for article in articles])

        print("Collected News Articles:")
        print(news_df)

        # Save as CSV
        news_df.to_csv("Supply_chain_news.csv", index=False)

        print("\nTop News Titles:")
        for idx, title in enumerate(news_df['Title'], start=1):
            print(f"{idx}. {title}")
    else:
        print("No articles found.")
else:
    print(f"Error: {response.status_code} - {response.text}")

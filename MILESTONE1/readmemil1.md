README - Supply Chain News Collection

Overview

This project fetches news articles related to supply chain disruptions and the sugar industry using the News API. The collected articles are processed and stored in a structured CSV format for further analysis.

Features

Automated News Retrieval: Fetches news articles based on predefined keywords.

Multi-Keyword Search: Searches for articles related to supply chain disruption, sugar supply, and sugar refining.

Data Storage: Saves collected articles into a CSV file for easy access and further processing.

Technologies Used

Python: Core programming language for API requests and data processing.

News API: Fetches real-time news articles.

Requests: Handles API requests.

Pandas: Processes and stores data in CSV format.

Code Workflow

1. News API Query

A list of predefined keywords is used to search for relevant news articles.

The script sends an API request for each keyword.

Articles are retrieved and stored if available.

2. Data Processing

Extracts key details such as title, description, source, published date, and URL.

Stores the data in a structured Pandas DataFrame.

3. Output Storage

The collected articles are saved as Supply_Chain_Impact_News.csv.

The script prints a list of the top news titles for quick review.

Output Files

Supply_Chain_Impact_News.csv: Contains the retrieved news articles with structured fields.

Usage Instructions

Install dependencies: requests, pandas.

Replace the api_key with a valid News API key.

Run the script to fetch and store news articles.

Review the generated CSV file for insights.

Future Enhancements

Implement additional NLP techniques for sentiment analysis.

Expand keyword searches to include broader supply chain topics.

Visualize trends in supply chain disruptions using dashboards.

This project helps track real-time supply chain news, providing valuable insights for analysis and decision-making.


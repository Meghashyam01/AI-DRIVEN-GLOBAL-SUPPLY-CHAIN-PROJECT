import pandas as pd
from transformers import pipeline

def initialize_sentiment_analyzer():
    """
    Initialize the sentiment analysis pipeline using Hugging Face's Transformers.
    """
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    return sentiment_pipeline

def analyze_inventory(data, sentiment_pipeline):
    """
    Analyze the inventory and make decisions based on warehouse data and sentiment analysis.
    """
    warehouse_capacity_threshold = 0.8  # 80% capacity considered high
    low_utilization_threshold = 0.4    # Below 40% is considered underutilized
    alerts = []

    for index, row in data.iterrows():
        # Calculate warehouse utilization
        utilization = row['Monthly Incoming (kg)'] / row['Warehouse Capacity (kg)']
        
        # Analyze sentiment from the data
        sentiment = sentiment_pipeline(row['Sentiment'])[0]
        sentiment_label = sentiment['label']  # Positive or Negative

        # Decision-making logic
        if utilization > warehouse_capacity_threshold:
            if sentiment_label == "NEGATIVE":
                alerts.append((row['Month'], "SELL", f"High utilization ({utilization:.2f}), negative sentiment detected"))
            else:
                alerts.append((row['Month'], "MONITOR", f"High utilization ({utilization:.2f}), but positive sentiment"))
        elif utilization < low_utilization_threshold:
            alerts.append((row['Month'], "BUY", f"Low utilization ({utilization:.2f}), consider buying materials"))
        elif row['Monthly Outgoing (kg)'] > row['Warehouse Capacity (kg)'] - row['Monthly Incoming (kg)']:
            alerts.append((row['Month'], "DEMAND EXCEEDS", f"Outgoing ({row['Monthly Outgoing (kg)']}) exceeds available stock"))

    return alerts

# Sample sugar product inventory data
data = {
    "Month": ["January", "February", "March", "April", "May"],
    "Warehouse Capacity (kg)": [10000] * 5,
    "Monthly Incoming (kg)": [8500, 9000, 4000, 7000, 9500],
    "Monthly Outgoing (kg)": [8000, 9500, 3000, 6000, 8500],
    "Sentiment": ["Neutral", "Negative", "Positive", "Neutral", "Negative"]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Initialize sentiment analyzer
sentiment_pipeline = initialize_sentiment_analyzer()

# Analyze inventory and display alerts
alerts = analyze_inventory(df, sentiment_pipeline)

# Display alerts
for alert in alerts:
    print(f"Month: {alert[0]}, Action: {alert[1]}, Reason: {alert[2]}")

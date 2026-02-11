# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load the data your bot has been logging
df = pd.read_csv("logs/market_data_log.csv")

# Create target: Did the price go up in the next bar? (1 = yes, 0 = no)
# We shift the close price to create the target
df = df.sort_values(['symbol', 'timestamp'])
df['next_close'] = df.groupby('symbol')['close_price'].shift(-1)
df['target'] = (df['next_close'] > df['close_price']).astype(int)

# Drop rows where we don't have next price
df = df.dropna()

# Features the AI will learn from
features = ['momentum', 'news_score', 'total_score']
X = df[features]
y = df['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple but powerful model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model trained! Accuracy: {accuracy:.2%}")

# Save the model
joblib.dump(model, "models/best_coin_model.pkl")
print("Model saved to models/best_coin_model.pkl")
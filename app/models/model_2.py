import random

def predict(file, params):
    # Mock predictions for testing
    mock_labels = ["apple", "banana", "orange", "grape", "strawberry"]
    prediction = random.choice(mock_labels)
    
    # Return a mock response with a random confidence score
    return {"label": prediction, "confidence": round(random.uniform(0.75, 0.95), 2)}

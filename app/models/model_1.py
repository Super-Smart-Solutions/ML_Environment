import random

def predict(file, params):
    # Mock predictions for testing
    mock_labels = ["cat", "dog", "car", "tree", "house"]
    prediction = random.choice(mock_labels)
    
    # Return a mock response with a random confidence score
    return {"label": prediction, "confidence": round(random.uniform(0.8, 1.0), 2)}

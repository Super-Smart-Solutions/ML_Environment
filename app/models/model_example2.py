import torch
from torchvision import models, transforms
from PIL import Image
from io import BytesIO

# Load the pre-trained ResNet18 model
model = models.resnet18(pretrained=True)
model.eval()  # Set the model to evaluation mode

# Define the image transformations
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Define the labels (ImageNet classes)
LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
labels = None

def load_labels():
    import urllib.request
    import json
    global labels
    with urllib.request.urlopen(LABELS_URL) as url:
        labels = json.loads(url.read().decode())

# Ensure labels are loaded
if labels is None:
    load_labels()

def predict(file, params):
    # Convert the uploaded file into a PIL image
    img = Image.open(BytesIO(file.read()))

    # Apply the preprocessing transformations
    img_t = preprocess(img)
    img_t = torch.unsqueeze(img_t, 0)  # Add a batch dimension

    # Make predictions
    with torch.no_grad():
        outputs = model(img_t)
    
    # Convert the outputs to probabilities
    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

    # Get the top 3 predictions
    top_probs, top_cats = torch.topk(probabilities, 3)
    results = [{"label": labels[idx], "confidence": prob.item()} for idx, prob in zip(top_cats, top_probs)]
    
    return {"predictions": results}

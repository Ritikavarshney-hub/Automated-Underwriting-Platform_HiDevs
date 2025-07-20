from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import os

app = FastAPI(title="AI Claims Automation System")

# Load BERT model and tokenizer (simulated fine-tuned version)
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=3)

def classify_claim(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    label = torch.argmax(outputs.logits).item()
    label_map = {0: "motor", 1: "health", 2: "property"}
    return label_map[label]

def determine_priority(text: str):
    return "high" if "emergency" in text.lower() or "surgery" in text.lower() else "normal"

def check_policy_compliance(text: str):
    if "alcohol" in text.lower():
        return False, "Claim contains exclusion keyword"
    return True, "Compliant with policy"

def route_claim(claim_type: str, priority: str):
    if priority == "high":
        return "fast-track team"
    if claim_type == "motor":
        return "motor claims team"
    return "general claims team"

def process_document(path: str):
    image = Image.open(path)
    text = pytesseract.image_to_string(image)
    return text

@app.post("/process-claim/")
async def process_claim(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = process_document(file_path)
    claim_type = classify_claim(text)
    priority = determine_priority(text)
    compliant, reason = check_policy_compliance(text)
    assigned = route_claim(claim_type, priority)

    os.remove(file_path)

    return JSONResponse({
        "extracted_text": text[:300] + "...",
        "claim_type": claim_type,
        "priority": priority,
        "policy_compliant": compliant,
        "compliance_reason": reason,
        "assigned_team": assigned
    })


# Run: uvicorn claim_automated_system:app --reload


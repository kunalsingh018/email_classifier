#Implementing API
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import uvicorn
import joblib
from masking import mask_full_pii_compliant 

#Load model and vectorizer
model = joblib.load("email_classifier_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

app = FastAPI()

class EmailRequest(BaseModel):
    email: str 

@app.post("/classify")
def classify_email(request: EmailRequest):
    raw_email = request.email

    #Masking PII and PCI
    masked_email, entities = mask_full_pii_compliant(raw_email)

    #Predicting category
    vectorized = vectorizer.transform([masked_email])
    predicted_category = model.predict(vectorized)[0]

    #Return in instructed format
    return {
        "input_email_body": raw_email,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": predicted_category
    }


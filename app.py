#Deployment on hugging face 
import gradio as gr
import joblib
import json
from masking import mask_full_pii_compliant

#Load model and vectorizer
model = joblib.load("email_classifier_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

def classify_email(email_text):
    masked_email, entities = mask_full_pii_compliant(email_text)
    vec = vectorizer.transform([masked_email])
    predicted = model.predict(vec)[0]

    result = {
        "input_email_body": email_text,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": predicted
    }

    return json.dumps(result, indent=2), masked_email, predicted

#Gradio UI
demo = gr.Interface(
    fn=classify_email,
    inputs=gr.Textbox(lines=20, label="Paste Support Email"),
    outputs=[
        gr.Textbox(label="Strict JSON Output"),
        gr.Textbox(label="Masked Email (Preview)"),
        gr.Textbox(label="Predicted Email Type")
    ],
    title="Support Email Classifier",
    description="Submit a raw support email. Get a strict JSON response + easy preview of the masked email and its category."
)

if __name__ == "__main__":
    demo.launch()

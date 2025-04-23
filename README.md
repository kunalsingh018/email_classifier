---
title: Email Classifier
sdk: gradio
sdk_version: 5.26.0
app_file: app.py
short_description: Akaike assignment
---

# 🛡️ Support Email Classifier with PII & PCI Masking

This project provides a secure, production-ready API for classifying customer support emails while masking all Personally Identifiable Information (PII) and Payment Card Industry (PCI) data — before any processing or classification takes place.

---

## 🚀 Features

- 🔐 Mask PII: Full Name, Email, Phone, DOB, Aadhar Number
- 💳 Mask PCI: Credit Card, Expiry, CVV
- 🧠 Classify emails into categories (e.g., Request, Incident, Billing Issues, etc.)
- ✅ Output follows strict required JSON structure
- 🖥️ Interactive Gradio UI (for deployment or demo)

---

## 📂 Repository Structure
├── app.py # Gradio frontend (Hugging Face Space entry)
├── masking.py # PII/PCI masking logic
├── email_classifier_model.pkl # Trained classification model
├── tfidf_vectorizer.pkl # TF-IDF vectorizer
├── input_data.csv # Raw training data
├── requirements.txt # All dependencies
└── README.md # This file

--- 
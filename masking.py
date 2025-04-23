import pandas as pd
import re
import json

def mask_full_pii_compliant(email_text):
    masked_email = email_text
    masked_entities = []
    

    def add_entity(match, ent_type):
        start, end = match.span(1)
        original = match.group(1).strip()
        masked = f"[{ent_type}]"
        nonlocal masked_email

        masked_email = masked_email[:start] + masked + masked_email[end:]

        return {
            "position": [start, start + len(masked)],
            "classification": ent_type,
            "entity": original
        }
#Patterns for masking
   
    context_patterns = [
        (r"\bmy name is\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)(?=[\.,\n]|$)", "full_name"),
        (r"(?i)\b(?:regards|sincerely|best(?: regards)?)\s*,?\s*\n([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)", "full_name"),
        (r"\breach me at\s+([\w\.-]+@[\w\.-]+\.\w+)", "email"),
        (r"\bmy contact number is\s+([+\d][\d\s\-().]{7,})", "phone_number"),
        (r"\bdate of birth\s*[:\-]?\s*(\d{2}[/-]\d{2}[/-]\d{2,4})", "dob"),
        (r"\baadhar(?: card)? number\s*[:\-]?\s*(\d{4}\s?\d{4}\s?\d{4})", "aadhar_num"),
        (r"\b(?:credit|debit)?\s*card number\s*[:\-]?\s*((?:\d{4}[ -]?){3,4})", "credit_debit_no"),
        (r"\bexpiry date is(?: date)?\s*[:\-]?\s*((?:0[1-9]|1[0-2])[/-]?\d{2,4})", "expiry_no"),
        (r"\bcvv is(?: number)?\s*[:\-]?\s*(\d{3})\b", "cvv_no")
    ]

    for pattern, ent_type in context_patterns:
        for match in re.finditer(pattern, masked_email, flags=re.IGNORECASE):
            masked_entities.append(add_entity(match, ent_type))

    return masked_email, masked_entities

#Load CSV
df = pd.read_csv("input_data.csv")

#Apply masking
def process_row(row):
    original_text = row["email"]
    category = row["type"]

    masked_email, entities = mask_full_pii_compliant(original_text)
    return json.dumps({
        "input_email_body": original_text,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": category
    })

    

df["json_output"] = df.apply(process_row, axis=1)

#Save JSONL file
df["json_output"].to_csv("masked_output_strict.jsonl", index=False, header=False)

print("✅ JSONL output saved as 'masked_output_strict.jsonl'")


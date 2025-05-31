 Medical Claim Denial Analysis – RCM Toolkit

This project is built to help *Medical Billing Analysts* and *RCM Teams* gain insights from claim data to reduce denials and improve collections.

📌 Purpose

Analyze medical billing Excel data (CPT codes, insurance, payments, etc.) to:
- Identify top denied CPTs
- Diagnose root causes of non-payment
- Recommend fixes for coding and workflow
- Generate visual reports for easy stakeholder review

---

📂 Features

✅ Analyze uploaded Excel file (e.g., `billing_data.xlsx`)  
✅ Detect denial trends by:
- *CPT Code*
- *Insurance Company*
- *Physician*

✅ Flag root causes like:
- Modifier issues
- LCD/NCD mismatches
- NCCI edits
- Missing documentation or authorizations

✅ Recommend fixes:
- Modifier adjustments
- Claim resubmission/appeals
- Documentation and workflow improvements

✅ Generate:
- Summary reports
- Denial trend charts
- Heat maps

---

🚀 How to Use

1. *Clone this repository*
2. *Install requirements*
   bash
   pip install -r requirements.txt
   
3. *Run the Streamlit App*
   bash
   streamlit run app.py
   ```

4. Upload your Excel file containing:
   - CPT Code
   - Insurance Company
   - Physician
   - Amount

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os

st.title("📄 Medical Claim Denial Analyzer & Predictor")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read uploaded file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    # Filter denied claims
    denied_claims = df[df['Payment'] == 0]

    # --- Tabs ---
    tab1, tab2 = st.tabs(["📊 Visualizations", "🔍 Batch Prediction"])

    # --- Tab 1: Visualizations ---
    with tab1:
        st.header("Claim Denial Visualizations")

        if denied_claims.empty:
            st.warning("No denied claims found in uploaded data.")
        else:
            # Top 10 Denied CPT Codes
            st.subheader("Top 10 Denied CPT Codes")
            denials_by_cpt = denied_claims.groupby("CPT Code").size().sort_values(ascending=False)
            plt.figure(figsize=(12, 6))
            denials_by_cpt.head(10).plot(kind='bar', color='coral')
            plt.title("Top 10 Denials by CPT Code")
            plt.ylabel("Denial Count")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(plt)

            # Denials by Payer
            st.subheader("Denials by Insurance Company")
            denials_by_payer = denied_claims.groupby("Insurance Company").size().sort_values(ascending=False)
            plt.figure(figsize=(12, 6))
            denials_by_payer.plot(kind='bar', color='skyblue')
            plt.title("Denials by Payer")
            plt.ylabel("Denial Count")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(plt)

            # Denials by Provider
            st.subheader("Denials by Provider")
            denials_by_provider = denied_claims.groupby("Physician").size().sort_values(ascending=False)
            plt.figure(figsize=(12, 6))
            denials_by_provider.plot(kind='bar', color='orange')
            plt.title("Denials by Provider")
            plt.ylabel("Denial Count")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(plt)

    # --- Tab 2: Prediction ---
    with tab2:
        st.header("Batch Prediction on Uploaded Data")

        model_path = os.path.join(os.getcwd(), 'denied_medclaim.pkl')
        encoder_path = os.path.join(os.getcwd(), 'frequency_encoder.pkl')

        required_cols = ['CPT Code', 'Insurance Company', 'Physician', 'Amount']

        if not all(col in df.columns for col in required_cols):
            missing_cols = [col for col in required_cols if col not in df.columns]
            st.error(f"Missing required columns: {', '.join(missing_cols)}")

        elif not os.path.exists(model_path):
            st.error("Model file not found. Please ensure 'denied_medclaim.pkl' is in the project folder.")

        elif not os.path.exists(encoder_path):
            st.error("Encoder file not found. Please ensure 'frequency_encoder.pkl' is in the project folder.")

        else:
            model = pickle.load(open(model_path, 'rb'))
            encoder = pickle.load(open(encoder_path, 'rb'))  # encoder is a dict

            # Copy relevant columns
            input_data = df[required_cols].copy()

            # Apply frequency encoding by mapping values using saved dict
            for col in ['Insurance Company', 'Physician']:
                input_data[col] = input_data[col].map(encoder[col]).fillna(0)

            # Predict using the model
            predictions = model.predict(input_data)

            df['Prediction'] = ["Denied" if p == 1 else "Not Denied" for p in predictions]

            st.success("Predictions completed.")
            st.dataframe(df[['CPT Code', 'Insurance Company', 'Physician', 'Amount', 'Prediction']])

            # Optional: Download results
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Prediction Results",
                data=csv,
                file_name='predicted_claims.csv',
                mime='text/csv'
            )
else:
    st.info("Please upload a file to begin.")
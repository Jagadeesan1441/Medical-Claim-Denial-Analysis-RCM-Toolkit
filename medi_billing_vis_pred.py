import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os

# --- Load Data ---
data_path = r"D:\medical_claim\newsynthetic_medical_billing.csv"
df = pd.read_csv(data_path)
denied_claims = df[df['Payment'] == 0]

# --- Tabs ---
tab1, tab2 = st.tabs(["📊 Visualizations", "🔍 Prediction"])

# --- Tab 1: Visualizations ---
with tab1:
    st.header("Claim Denial Visualizations")

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
    st.header("Medical Claim Denial Predictor")

    model_path = os.path.join(os.getcwd(), 'deniedlast.pkl')
    encoder_path = os.path.join(os.getcwd(), 'encodernew3.pkl')

    unique_cpts = df['CPT Code'].unique().tolist()
    insurance_companies = df['Insurance Company'].unique().tolist()
    physicians = df['Physician'].unique().tolist()

    if not os.path.exists(model_path):
        st.error("Model file not found. Please ensure 'deniednew.pkl' is in the project folder.")
    elif not os.path.exists(encoder_path):
        st.error("Encoder file not found. Please ensure 'encodernew2.pkl' is in the project folder.")
    else:
        model = pickle.load(open(model_path, 'rb'))
        encoder = pickle.load(open(encoder_path, 'rb'))

        # Input form
        cpt = st.selectbox("Select CPT Code", unique_cpts)
        insurance = st.selectbox("Select Insurance Company", insurance_companies)
        physician = st.selectbox("Select Physician", physicians)
        amount = st.number_input("Enter Claim Amount", min_value=0.0, step=10.0)

        if st.button("Predict"):
            # Create input dataframe
            input_df = pd.DataFrame({
                'CPT Code': [cpt],
                'Insurance Company': [insurance],
                'Physician': [physician],
                'Amount': [amount]
            })

            # Encode categorical features (excluding CPT Code and Amount)
            encoded_cols = encoder.transform(input_df[['Insurance Company', 'Physician']])
            input_df[['Insurance Company', 'Physician']] = encoded_cols

            # If CPT Code also needs encoding, handle it here (if required by your model)
            # If model expects CPT Code as-is (string or number), leave it unchanged

            # Predict
            prediction = model.predict(input_df)[0]
            result = "Denied" if prediction == 1 else "Not Denied"
            st.success(f"Prediction: {result}")
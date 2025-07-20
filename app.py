import streamlit as st
import requests

st.title("AI-Powered Insurance Claim Processor")

uploaded_file = st.file_uploader("Upload Claim Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    if st.button("Process Claim"):
        with st.spinner("Processing..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post("https://ideal-fiesta-8000.app.github.dev/process-claim/", files=files)

            if response.status_code == 200:
                result = response.json()
                st.success("Claim Processed Successfully!")
                st.write("**Extracted Text:**", result["extracted_text"])
                st.write("**Claim Type:**", result["claim_type"])
                st.write("**Priority:**", result["priority"])
                st.write("**Compliant:**", result["policy_compliant"])
                st.write("**Reason:**", result["compliance_reason"])
                st.write("**Assigned Team:**", result["assigned_team"])
            else:
                st.error("❌ Failed to process claim. Check backend API.")



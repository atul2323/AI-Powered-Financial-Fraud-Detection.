import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-PoweredFinancial Fraud-Detection
",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main-title {
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#1E88E5;
}
.subtitle {
    text-align:center;
    color:gray;
    margin-bottom:20px;
}
.feature-box{
    padding:20px;
    border-radius:10px;
    background-color:#f5f5f5;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<p class="main-title">🛡️ AI FRAUD DETECTION</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI Powered Financial Fraud Detection System</p>', unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("☰ FEATURES")

feature = st.sidebar.radio(
    "",
    [
        "🏠 Dashboard",
        "💳 Transaction Detection",
        "📷 QR Code Detection",
        "🌐 Fraud Website Detection",
        "📱 UPI ID Detection",
        "🕸️ Fraud Network Analysis",
        "🤖 AI Chatbot"
    ]
)

# ---------------- LAYOUT ----------------
left,right = st.columns([3,1])

# ================= RIGHT PANEL =================
with right:

    st.subheader("📊 Real-Time Risk Score")

    risk_score = 78

    st.metric(
        label="Current Risk",
        value=f"{risk_score}%"
    )

    st.progress(risk_score)

    if risk_score < 30:
        st.success("LOW RISK")
    elif risk_score < 70:
        st.warning("MEDIUM RISK")
    else:
        st.error("HIGH RISK")

    st.markdown("---")

    st.subheader("⚠ Risk Factors")

    st.write("• Device Risk")
    st.write("• IP Risk")
    st.write("• Location Risk")
    st.write("• Transaction Pattern")
    st.write("• Behavioral Analysis")

# ================= MAIN CONTENT =================
with left:

    # DASHBOARD
    if feature == "🏠 Dashboard":

        st.header("Dashboard")

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Transactions", "10,245")
        c2.metric("Frauds Detected", "342")
        c3.metric("Detection Rate", "96.8%")
        c4.metric("Money Saved", "$45,200")

        st.markdown("---")

        st.subheader("System Features")

        st.info("💳 Normal Transaction Detection")
        st.info("📷 QR Code Fraud Detection")
        st.info("🌐 Fraud Website Detection")
        st.info("📱 UPI ID Fraud Detection")
        st.info("🕸️ Fraud Network Analysis")
        st.info("🤖 AI Fraud Assistant")

    # TRANSACTION DETECTION
    elif feature == "💳 Transaction Detection":

        st.header("💳 Transaction Fraud Detection")

        amount = st.number_input("Transaction Amount")

        transaction_type = st.selectbox(
            "Transaction Type",
            ["UPI","Card","Bank Transfer","Wallet"]
        )

        merchant = st.text_input("Merchant Name")

        location = st.text_input("Location")

        if st.button("Analyze Transaction"):

            st.success("Prediction Complete")

            st.metric(
                "Fraud Probability",
                "82%"
            )

            st.error("Potential Fraud Detected")

    # QR DETECTION
    elif feature == "📷 QR Code Detection":

        st.header("📷 QR Code Fraud Detection")

        uploaded_file = st.file_uploader(
            "Upload QR Code",
            type=["png","jpg","jpeg"]
        )

        if uploaded_file:

            st.image(uploaded_file,width=300)

            if st.button("Scan QR"):

                st.success("QR Processed")

                st.metric(
                    "Fraud Score",
                    "73%"
                )

                st.error("Suspicious QR Detected")

    # WEBSITE DETECTION
    elif feature == "🌐 Fraud Website Detection":

        st.header("🌐 Fraud Website Detection")

        url = st.text_input("Enter Website URL")

        if st.button("Check Website"):

            st.metric(
                "Risk Score",
                "88%"
            )

            st.error("Phishing Website Detected")

    # UPI DETECTION
    elif feature == "📱 UPI ID Detection":

        st.header("📱 UPI ID Fraud Detection")

        upi = st.text_input(
            "Enter UPI ID",
            placeholder="abc@paytm"
        )

        if st.button("Verify UPI"):

            st.metric(
                "Risk Score",
                "67%"
            )

            st.warning("Suspicious UPI ID")

    # NETWORK ANALYSIS
    elif feature == "🕸️ Fraud Network Analysis":

        st.header("🕸️ Fraud Network Analysis")

        G = nx.Graph()

        G.add_edges_from([
            ("User A","Device X"),
            ("User B","Device X"),
            ("User C","Device Y"),
            ("User D","Device Z")
        ])

        fig, ax = plt.subplots(figsize=(8,5))
        nx.draw(
            G,
            with_labels=True,
            ax=ax
        )

        st.pyplot(fig)

        st.success(
            "Shared Device X may indicate fraudulent activity."
        )

    # CHATBOT
    elif feature == "🤖 AI Chatbot":

        st.header("🤖 AI Fraud Assistant")

        user_query = st.text_input(
            "Ask Anything About Fraud Detection"
        )

        if st.button("Send"):

            st.info(
                f"You Asked: {user_query}"
            )

            st.success(
                "Connect your Gemini/OpenAI model here."
            )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("AI Fraud Detection System © 2026")

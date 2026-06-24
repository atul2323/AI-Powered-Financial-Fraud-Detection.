import streamlit as st
import plotly.graph_objects as go
import time

# --------------------------------------------------------
# PAGE CONFIGURATION & HEADER
# --------------------------------------------------------
st.set_page_config(
    page_title="AI Fraud Detection Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header [cite: 21]
st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; padding: 10px 0px; border-bottom: 2px solid #f0f2f6; margin-bottom: 25px;'>
        <div style='display: flex; align-items: center;'>
            <h1 style='margin: 0; color: #FF4B4B; font-size: 2rem;'>🛡️ AI FRAUD DETECTION</h1>
        </div>
        <div>
            <span style='font-size: 1.5rem; cursor: pointer; position: relative;'>
                🔔<span style='position: absolute; top: -5px; right: -5px; background-color: red; color: white; border-radius: 50%; padding: 2px 6px; font-size: 10px;'>3</span>
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# SIDEBAR NAVIGATION [cite: 4, 22]
# --------------------------------------------------------
st.sidebar.title("Navigation Menu")
menu_option = st.sidebar.radio(
    "Select Fraud Detection Module:",
    [
        "📊 Dashboard Overview",
        "💳 Normal Transaction Detection",
        "🔲 QR Code Detection",
        "🌐 Fraud Website Detection",
        "🆔 UPI ID Detection",
        "🕸️ Fraud Network Analysis",
        "🤖 AI Chatbot"
    ]
)

# --------------------------------------------------------
# HELPER FUNCTION FOR RISK METER (RIGHT PANEL) [cite: 9, 36]
# --------------------------------------------------------
def render_risk_meter(score, level, factors):
    st.subheader("📊 Real-Time Transaction Risk Score") [cite: 33]
    
    # Gauge chart using Plotly [cite: 9, 36]
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Risk Level: {level}", 'font': {'size': 18}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#222222"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 35], 'color': '#2ecc71'},
                {'range': [35, 70], 'color': '#f1c40f'},
                {'range': [70, 100], 'color': '#e74c3c'}
            ],
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
    
    # Explanation [cite: 37]
    st.markdown("### 🔍 Risk Factor Breakdown") [cite: 37]
    for factor in factors:
        st.markdown(f"- {factor}") [cite: 37]

# --------------------------------------------------------
# MAIN LAYOUT SPLIT (Main Workspace vs Right Panel) [cite: 4, 30, 32]
# --------------------------------------------------------
main_col, right_col = st.columns([2.2, 1])

# Global defaults for the right panel to show real-time changes
current_score = 12
current_level = "LOW"
current_factors = ["Transaction originates from a recognized device.", "Standard pattern matching consistent with baseline user behavior."]

# --------------------------------------------------------
# MODULE LOGIC [cite: 14, 15, 16]
# --------------------------------------------------------

with main_col:
    # 1. Dashboard Overview [cite: 23]
    if menu_option == "📊 Dashboard Overview":
        st.title("Welcome to AI Fraud Detection Hub") [cite: 13]
        st.write("Real-time monitoring and malicious activity detection terminal.")
        
        # Display summary cards
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Monitored Today", "14,250", "+12%")
        c2.metric("Flagged Anomalies", "34", "-5%")
        c3.metric("System Health", "99.8%", "Optimal")
        
        st.info("💡 Select a module from the left sidebar menu to begin target evaluation.") [cite: 14]

    # 2. Normal Transaction Detection [cite: 5, 24]
    elif menu_option == "💳 Normal Transaction Detection":
        st.title("💳 Normal Transaction Analysis") [cite: 5, 24]
        st.write("Evaluate standard fiat transactions for multi-vector risk profiling.") [cite: 31]
        
        with st.form("transaction_form"): [cite: 31]
            sender = st.text_input("Sender Account Number", placeholder="e.g., ACC12345678") [cite: 31]
            receiver = st.text_input("Receiver Account Number", placeholder="e.g., ACC87654321") [cite: 31]
            amount = st.number_input("Transaction Amount ($)", min_value=0.0, step=10.0) [cite: 31]
            tx_type = st.selectbox("Transaction Type", ["TRANSFER", "CASH_OUT", "PAYMENT", "DEBIT"]) [cite: 31]
            submit = st.form_submit_with_button("Analyze Transaction")
            
            if submit:
                # Simulated Result Generation [cite: 31]
                if amount > 10000:
                    current_score = 85
                    current_level = "HIGH"
                    current_factors = ["High liquidity outbound velocity.", "Unusual transaction size for this time window.", "Cross-border destination routing."]
                else:
                    current_score = 24
                    current_level = "LOW"
                    current_factors = ["Standard velocity metrics.", "Known trusted counterparty network verification."]
                
                st.success(f"Analysis Complete. Resulting Risk Level: {current_level} ({current_score}%)") [cite: 31]

    # 3. QR Code Detection [cite: 6, 25]
    elif menu_option == "🔲 QR Code Detection":
        st.title("🔲 Malicious QR Code Scanner") [cite: 6, 25]
        st.write("Scan and decode QR targets to filter for hidden redirect payloads or phishing exploits.") [cite: 31]
        
        uploaded_file = st.file_uploader("Upload QR Code Image Asset", type=["png", "jpg", "jpeg"]) [cite: 31]
        qr_text_fallback = st.text_input("Or paste raw decoded QR string payload data:") [cite: 31]
        
        if uploaded_file or qr_text_fallback:
            with st.spinner("Deconstructing QR Payload Content..."):
                time.sleep(1)
            # Simulated outcome
            current_score = 72
            current_level = "HIGH"
            current_factors = ["QR string points to an unverified shortcut short-URL.", "Domain utilizes look-alike typo-squatting characters."]
            st.warning("⚠️ Warning: QR metadata references potentially hazardous destination targets.") [cite: 31]

    # 4. Fraud Website Detection [cite: 7, 26]
    elif menu_option == "🌐 Fraud Website Detection":
        st.title("🌐 Website Trustworthiness & Phishing Check") [cite: 7, 26]
        st.write("Inspect external hyperlinks against live algorithmic risk score indexes.") [cite: 31]
        
        target_url = st.text_input("Enter Web URL Target Address:", placeholder="https://secure-bank-login-verification.com") [cite: 31]
        if st.button("Evaluate Domain"): [cite: 31]
            if "secure-bank" in target_url:
                current_score = 94
                current_level = "HIGH"
                current_factors = ["Domain registered < 48 hours ago.", "Exhibits brand impersonation tactics.", "SSL certificate issued via untrusted authority."]
                st.error("🚨 Highly Probable Phishing Vector Detected!") [cite: 31]
            else:
                current_score = 8
                current_level = "LOW"
                current_factors = ["Established Alexa Top 5k ranking index.", "Long-standing domain history verification."]
                st.success("✅ Clean Record: Domain checks match trusted baseline indexes.") [cite: 31]

    # 5. UPI ID Detection [cite: 8, 27]
    elif menu_option == "🆔 UPI ID Detection":
        st.title("🆔 UPI ID Risk Assessment") [cite: 8, 27]
        st.write("Verify Virtual Payment Addresses (VPAs) against spam indexes and dynamic chargeback profiles.") [cite: 31]
        
        upi_id = st.text_input("Target UPI ID / VPA:", placeholder="username@bankhandle") [cite: 31]
        if st.button("Query UPI Endpoint"): [cite: 31]
            if "hack" in upi_id or "spam" in upi_id:
                current_score = 68
                current_level = "MEDIUM"
                current_factors = ["VPA reported via user community flags.", "Elevated volume of transaction reversal attempts."]
                st.warning("⚠️ Caution: UPI ID exhibits abnormal chargeback frequencies.") [cite: 31]
            else:
                current_score = 15
                current_level = "LOW"
                current_factors = ["KYC Verified merchant account.", "Clean routing verification."]
                st.success("✅ VPA Verified Secure.") [cite: 31]

    # 6. Fraud Network Analysis [cite: 9, 28]
    elif menu_option == "🕸️ Fraud Network Analysis":
        st.title("🕸️ Graph Fraud Network Analysis") [cite: 9, 28]
        st.write("Visualize entity association mapping networks to see multi-hop syndicates.") [cite: 18]
        
        # Displaying a mock network connection mapping graph using Streamlit Graphviz
        st.graphviz_chart('''
        digraph {
            "Target User" -> "Mule Account A" [label="High Velocity Transfer"]
            "Target User" -> "Mule Account B" [label="Splitting Structure"]
            "Mule Account A" -> "Known Offshore Mixer" [color=red, penwidth=2.0]
            "Mule Account B" -> "Known Offshore Mixer" [color=red, penwidth=2.0]
            "Suspicious IP Node" -> "Target User" [style=dotted]
        }
        ''') [cite: 18]
        
        current_score = 78
        current_level = "HIGH"
        current_factors = ["Connected multi-hop dependencies to flagged wallets.", "Layering behavior mapping matches money laundering blueprints."]

    # 7. AI Chatbot Explanation [cite: 10, 29]
    elif menu_option == "🤖 AI Chatbot":
        st.title("🤖 Fraud Insights AI Assistant") [cite: 10, 29]
        st.write("Inquire regarding model reasoning variables, rulesets, or mitigation procedures.") [cite: 19]
        
        # Initialize session state for simple structural message persistence
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hello, I am your fraud analyst AI. Ask me about flagged scores or suspicious network graphs."}] [cite: 19]
            
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
            
        if user_query := st.chat_input("Ask a question about the fraud analysis..."): [cite: 19]
            st.session_state.messages.append({"role": "user", "content": user_query}) [cite: 19]
            st.chat_message("user").write(user_query) [cite: 19]
            
            # Simple fallback responses [cite: 19]
            ai_response = "Based on our model parameters, the transaction flags are determined using a mix of device fingerprint anomalies, velocity checks, and graph path matching algorithms." [cite: 19]
            st.session_state.messages.append({"role": "assistant", "content": ai_response}) [cite: 19]
            st.chat_message("assistant").write(ai_response) [cite: 19]

# --------------------------------------------------------
# RENDERING THE CONTINUOUS RIGHT PANEL RISK RADAR [cite: 17, 32]
# --------------------------------------------------------
with right_col:
    st.markdown("---")
    # Wrap in a stylized card container
    with st.container():
        render_risk_meter(current_score, current_level, current_factors) [cite: 8, 9, 34, 35, 36, 37]

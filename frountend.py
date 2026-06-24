import streamlit as st
import plotly.graph_objects as go
import time

# --------------------------------------------------------
# PAGE CONFIGURATION & THEME
# --------------------------------------------------------
st.set_page_config(
    page_title="AI-Powered Financial Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve UI depth, whitespace, and layout card padding
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 700;
        }
        .main-header {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 15px 25px;
            border-radius: 12px;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        .risk-card {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------------
# This keeps track of risk states globally so the right-side gauge
# updates dynamically as the user interacts with the app features.
if "risk_score" not in st.session_state:
    st.session_state.risk_score = 15
if "risk_level" not in st.session_state:
    st.session_state.risk_level = "LOW"
if "risk_factors" not in st.session_state:
    st.session_state.risk_factors = [
        "Device fingerprint verified matches typical user device profile.",
        "IP routing verification shows stable geolocation footprint."
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I am your AI Fraud Analyst. You can ask me to explain risk factor profiles, suspicious connections, or UPI anomaly models."}
    ]

# --------------------------------------------------------
# HEADER HEADER SECTION
# --------------------------------------------------------
st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 2rem;">🛡️</span>
            <div>
                <h2 style="margin: 0; color: #ff4b4b; font-size: 1.6rem; font-weight: 800; letter-spacing: 0.5px;">AI FRAUD DETECTION</h2>
                <p style="margin: 0; color: #94a3b8; font-size: 0.8rem;">Cognitive Financial Crime Shield Terminal</p>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="background: #334155; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                🟢 SYSTEM STATUS: ACTIVE
            </div>
            <div style="position: relative; cursor: pointer;">
                <span style="font-size: 1.5rem;">🔔</span>
                <span style="position: absolute; top: -2px; right: -2px; background: #ef4444; color: white; border-radius: 50%; font-size: 9px; padding: 1px 5px; font-weight: bold;">3</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------------
st.sidebar.markdown("### 🎛️ Navigation Menu")
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
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛡️ Secure Core Version")
st.sidebar.info("Model Engine v2.5-Live\nLast Sync: Just Now")

# --------------------------------------------------------
# HELPER ACTIONS TO UPDATE GLOBALLY TRACKED STATE
# --------------------------------------------------------
def update_risk_profile(score, level, factors):
    st.session_state.risk_score = score
    st.session_state.risk_level = level
    st.session_state.risk_factors = factors

# --------------------------------------------------------
# TWO-COLUMN MAIN CONTENT SPLIT
# --------------------------------------------------------
main_col, right_col = st.columns([1.8, 1])

with main_col:
    # --------------------------------------------------------
    # 1. Dashboard Overview
    # --------------------------------------------------------
    if menu_option == "📊 Dashboard Overview":
        st.subheader("📊 System-wide Overview Dashboard")
        st.write("Live status telemetry feed of transaction patterns and flagged vector groups.")
        
        # Statistics Row
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Transactions Scanned", "148,930", "+14% vs yesterday", delta_color="normal")
        with m2:
            st.metric("Anomalies Flagged", "42", "2.1% target rate", delta_color="inverse")
        with m3:
            st.metric("Average Threat Response", "48ms", "AI pipeline latency", delta_color="normal")
            
        st.markdown("---")
        st.markdown("### Recent System Incidents")
        st.dataframe([
            {"Timestamp": "14:24:02", "Vector": "UPI ID Anomaly", "VPA Target": "rewards-refund@paytm", "Risk Score": "84%", "Action": "Auto-Hold"},
            {"Timestamp": "14:21:15", "Vector": "Normal Transaction", "Account": "ACC-99812", "Risk Score": "24%", "Action": "Approved"},
            {"Timestamp": "14:15:33", "Vector": "Fraud Domain", "URL Target": "http://bank-verification-ssl.com", "Risk Score": "96%", "Action": "Blacklisted"},
            {"Timestamp": "14:02:49", "Vector": "QR Exploitation", "Payload Source": "Mule VPA Redirect", "Risk Score": "71%", "Action": "User Alerted"}
        ], use_container_width=True)

    # --------------------------------------------------------
    # 2. Normal Transaction Detection
    # --------------------------------------------------------
    elif menu_option == "💳 Normal Transaction Detection":
        st.subheader("💳 Fiat Transaction Analyzer")
        st.write("Scan physical or fiat ledger transfer parameters via multi-vector anomaly engines.")
        
        with st.form("transaction_form"):
            sender = st.text_input("Sender Account VPA or Number", placeholder="e.g., ACC-778103")
            receiver = st.text_input("Receiver Account VPA or Number", placeholder="e.g., ACC-114256")
            amount = st.number_input("Transaction Volume ($ USD)", min_value=0.0, step=100.0, format="%.2f")
            tx_type = st.selectbox("Routing Layer Engine", ["WIRE TRANSFER", "MERCHANT PAY", "P2P CASH-OUT", "DEBIT DIRECT"])
            
            submit = st.form_submit_with_button("Analyze Transaction")
            
            if submit:
                with st.spinner("Calculating threat parameters..."):
                    time.sleep(0.6)
                if amount > 15000:
                    update_risk_profile(
                        score=88,
                        level="HIGH",
                        factors=[
                            "Transaction volume exceeds typical historic baseline by 400%.",
                            "Unusual high-liquidity destination routing layer selected.",
                            "Suspicious immediate cash-out route signature."
                        ]
                    )
                    st.error("🚨 Highly High-Risk parameters detected! Transaction held.")
                elif amount > 5000:
                    update_risk_profile(
                        score=54,
                        level="MEDIUM",
                        factors=[
                            "Intermediary tier transfer parameters detected.",
                            "Routing velocity profile is elevated for this hour."
                        ]
                    )
                    st.warning("⚠️ Medium risk score registered. Secondary authorization recommended.")
                else:
                    update_risk_profile(
                        score=14,
                        level="LOW",
                        factors=[
                            "Standard secure transfer size parameters.",
                            "Trusted transfer destination with no negative history."
                        ]
                    )
                    st.success("✅ Clean baseline signatures. Transaction cleared!")

    # --------------------------------------------------------
    # 3. QR Code Detection
    # --------------------------------------------------------
    elif menu_option == "🔲 QR Code Detection":
        st.subheader("🔲 QR Decryption & Spoofing Defense")
        st.write("Upload static printed QR codes to scan embedded links for script injection or redirection routes.")
        
        uploaded_file = st.file_uploader("Upload QR Code Image Target", type=["png", "jpg", "jpeg"])
        raw_qr_data = st.text_input("Or input raw extracted QR payload string directly:")
        
        if uploaded_file or raw_qr_data:
            with st.spinner("Extracting hidden metadata packets..."):
                time.sleep(0.8)
            
            # Analyze contents for phishing/spoofing indicators
            payload = raw_qr_data if raw_qr_data else "https://shorturl.at/xK98a-secure-verification"
            if "shorturl" in payload or "secure-verification" in payload or "bit.ly" in payload:
                update_risk_profile(
                    score=76,
                    level="HIGH",
                    factors=[
                        "Embedded URL maps through an untrusted domain shortener.",
                        "String analysis contains high confidence banking keywords masquerading as target VPA."
                    ]
                )
                st.error("🚨 Malicious QR Payload Indicator Triggered!")
            else:
                update_risk_profile(
                    score=18,
                    level="LOW",
                    factors=[
                        "QR string successfully maps to verified merchant gateway directly."
                    ]
                )
                st.success("✅ Secure QR code signature. Proceed securely.")

    # --------------------------------------------------------
    # 4. Fraud Website Detection
    # --------------------------------------------------------
    elif menu_option == "🌐 Fraud Website Detection":
        st.subheader("🌐 Website Reputation & Phishing URL Check")
        st.write("Evaluate domain registration dates, hosting nameservers, and spelling vectors for high-risk flags.")
        
        target_domain = st.text_input("Target Domain URL Address", placeholder="http://login-verification-paypal-security.com")
        
        if st.button("Query Domain Database"):
            if not target_domain:
                st.info("Please enter a domain URL to run live audits.")
            else:
                with st.spinner("Scanning DNS records, WHOIS database, and certificate trails..."):
                    time.sleep(1.0)
                
                # Dynamic matching heuristic simulation
                suspicious_keywords = ["secure", "bank", "login", "verification", "update", "paypal", "support"]
                found_flags = [kw for kw in suspicious_keywords if kw in target_domain.lower()]
                
                if len(found_flags) >= 2 or ".net" in target_domain or ".xyz" in target_domain:
                    update_risk_profile(
                        score=91,
                        level="HIGH",
                        factors=[
                            f"Domain matches multiple high-risk typo-squatting keyphrases: {found_flags}.",
                            "SSL Certificate authority is unrecognized or missing.",
                            "Domain created within the last 72 hours."
                        ]
                    )
                    st.error("🚨 Phishing Target Vector Verified!")
                else:
                    update_risk_profile(
                        score=11,
                        level="LOW",
                        factors=[
                            "Domain registered with recognized high-trust authority.",
                            "Establishment timeline exceeds 1200 days verification index."
                        ]
                    )
                    st.success("✅ Domain verified clean. No indicators of threat found.")

    # --------------------------------------------------------
    # 5. UPI ID Detection
    # --------------------------------------------------------
    elif menu_option == "🆔 UPI ID Detection":
        st.subheader("🆔 Virtual Payment Address (VPA) Threat Auditor")
        st.write("Query UPI handles against crowd-sourced spamlists and instant transaction reversal metrics.")
        
        target_vpa = st.text_input("VPA UPI Handle Address", placeholder="e.g., trust-claims@freecharge")
        
        if st.button("Evaluate UPI Address"):
            if not target_vpa:
                st.info("Input a payment address VPA to check reputation.")
            else:
                with st.spinner("Requesting historical spam databases..."):
                    time.sleep(0.5)
                
                if "free" in target_vpa.lower() or "spam" in target_vpa.lower() or "cash" in target_vpa.lower():
                    update_risk_profile(
                        score=69,
                        level="MEDIUM",
                        factors=[
                            "Handle reported in 12 independent spam flag groups.",
                            "VPA contains high-frequency refund attempt anomalies.",
                            "Mule account registration flag on associated UPI system bank."
                        ]
                    )
                    st.warning("⚠️ Spammed UPI destination found. Hold highly suggested.")
                else:
                    update_risk_profile(
                        score=9,
                        level="LOW",
                        factors=[
                            "Fully verified KYC account owner confirmation.",
                            "UPI velocity rates within standard local brackets."
                        ]
                    )
                    st.success("✅ Account verified safe.")

    # --------------------------------------------------------
    # 6. Fraud Network Analysis
    # --------------------------------------------------------
    elif menu_option == "🕸️ Fraud Network Analysis":
        st.subheader("🕸️ Dynamic Fraud Association Graph Graph viz")
        st.write("This graphical network exposes connected entities, mules, and untrustworthy foreign mixers mapping to the target ID.")
        
        # Draw clean Graphviz path representation
        st.graphviz_chart('''
        digraph {
            node [style=filled, shape=box, fontname="Helvetica", fontsize=10];
            "Target Transaction ID" [fillcolor="#ffb3b3", color="#ff4d4d", label="Suspicious Transaction\\n(Score: 84%)"];
            "Mule Wallet Alpha" [fillcolor="#ffe6b3", label="Mule Wallet Alpha\\n(Flagged IP)"];
            "Trusted Merchant Account" [fillcolor="#d1e7dd", label="Trusted Portal\\n(Verified KYC)"];
            "Offshore Asset Mixer" [fillcolor="#f8d7da", color="#dc3545", label="Offshore Mixer\\n(Blacklisted Address)"];
            
            "Target Transaction ID" -> "Mule Wallet Alpha" [label="Rapid Split-Layering"];
            "Target Transaction ID" -> "Trusted Merchant Account" [label="Valid Check"];
            "Mule Wallet Alpha" -> "Offshore Asset Mixer" [color="#dc3545", style=bold, label="Exfiltration Pathway"];
        }
        ''')
        
        update_risk_profile(
            score=84,
            level="HIGH",
            factors=[
                "High proximity relationship to documented offshore mixers.",
                "Structure splitting signatures matching rapid asset exfiltration strategies."
            ]
        )
        st.info("💡 Review the visualization to identify layering strategies and exit accounts.")

    # --------------------------------------------------------
    # 7. AI Chatbot
    # --------------------------------------------------------
    elif menu_option == "🤖 AI Chatbot":
        st.subheader("🤖 Cognitive Fraud Insights Assistant")
        st.write("Understand AI threat logic, receive explanation of variables, or request defensive next steps.")
        
        # Chat log render loop
        for chat in st.session_state.chat_history:
            with st.chat_message(chat["role"]):
                st.write(chat["content"])
                
        user_input = st.chat_input("Ask how risk parameters are calculated...")
        
        if user_input:
            # Append query
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
                
            # Simulate analytical system generation
            with st.spinner("AI analyzing profile conditions..."):
                time.sleep(0.7)
                
            # Informative response
            ai_response = f"Analyzing your query relative to active parameters (Risk Score: {st.session_state.risk_score}%, Risk Level: {st.session_state.risk_level}). This threat rating is primarily driven by: {', '.join(st.session_state.risk_factors)}. To secure this path, I advise isolating the destination address and executing immediate transaction rollbacks."
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            with st.chat_message("assistant"):
                st.write(ai_response)

# --------------------------------------------------------
# RENDERING THE CONTINUOUS RIGHT PANEL RISK RADAR
# --------------------------------------------------------
with right_col:
    st.markdown('<div class="risk-card">', unsafe_allow_html=True)
    st.subheader("🛡️ Real-Time Risk Radar")
    st.write("Evaluations adjust automatically dynamically based on live workspace interactions.")
    
    # Calculate gauge bar color based on level
    bar_color = "#2ecc71"  # green
    if st.session_state.risk_level == "MEDIUM":
        bar_color = "#f1c40f"  # yellow
    elif st.session_state.risk_level == "HIGH":
        bar_color = "#e74c3c"  # red
        
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=st.session_state.risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': bar_color},
            'bgcolor': "#e2e8f0",
            'borderwidth': 1,
            'bordercolor': "#cbd5e1",
            'steps': [
                {'range': [0, 35], 'color': '#f1f5f9'},
                {'range': [35, 70], 'color': '#fef3c7'},
                {'range': [70, 100], 'color': '#fee2e2'}
            ],
        }
    ))
    fig.update_layout(
        height=220,
        margin=dict(l=15, r=15, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Status level badge
    level_color_map = {"LOW": "#d1e7dd", "MEDIUM": "#fff3cd", "HIGH": "#f8d7da"}
    text_color_map = {"LOW": "#0f5132", "MEDIUM": "#664d03", "HIGH": "#842029"}
    st.markdown(f"""
        <div style="text-align: center; background-color: {level_color_map[st.session_state.risk_level]}; color: {text_color_map[st.session_state.risk_level]}; padding: 8px; border-radius: 8px; font-weight: bold; font-size: 1.1rem; margin-bottom: 20px;">
            RISK ASSESSMENT: {st.session_state.risk_level}
        </div>
    """, unsafe_allow_html=True)
    
    # Active threat factors
    st.markdown("##### 🔬 Threat Vector Factors:")
    for idx, factor in enumerate(st.session_state.risk_factors, 1):
        st.markdown(f"**{idx}.** {factor}")
        
    st.markdown('</div>', unsafe_allow_html=True)

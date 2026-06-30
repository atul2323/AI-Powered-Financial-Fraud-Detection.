import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="Sentinel | AI Fraud Intelligence Platform",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# DESIGN SYSTEM
# ==========================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    :root{
        --ink-950:#0a0e16; --ink-900:#10151f; --ink-800:#161d2b;
        --ink-700:#1e2738; --ink-600:#2a3548; --line:#243044;
        --text-hi:#eef2f8; --text-mid:#9aa7bd; --text-low:#5e6b82;
        --accent:#3dd6c4; --accent-dim:#1e8b7e; --violet:#a78bfa;
        --warn:#f5b84e; --danger:#ef5d6f; --ok:#3dd6c4; --radius:14px;
    }
    html, body, [class*="css"]{ font-family:'Inter', -apple-system, sans-serif; }
    .stApp{
        background:
            radial-gradient(900px 500px at 85% -10%, rgba(61,214,196,0.07), transparent 60%),
            radial-gradient(700px 450px at 5% 10%, rgba(167,139,250,0.05), transparent 60%),
            var(--ink-950);
    }
    .block-container{ padding-top:1.2rem; padding-bottom:2rem; max-width:1500px; }
    section[data-testid="stSidebar"]{ background:var(--ink-900); border-right:1px solid var(--line); }
    section[data-testid="stSidebar"] .block-container{ padding-top:1.6rem; }

    /* ---- top bar ---- */
    .topbar{
        background:linear-gradient(180deg, var(--ink-800) 0%, var(--ink-900) 100%);
        border:1px solid var(--line); border-radius:var(--radius);
        padding:18px 26px; margin-bottom:22px;
        display:flex; justify-content:space-between; align-items:center;
    }
    .brand-mark{
        width:42px;height:42px;border-radius:10px;
        background:linear-gradient(135deg, var(--accent), var(--accent-dim));
        display:flex;align-items:center;justify-content:center;
        font-weight:800;font-size:1.1rem;color:#06231f; flex-shrink:0;
    }
    .brand-name{ margin:0;color:var(--text-hi);font-size:1.32rem;font-weight:800;letter-spacing:-0.01em; }
    .brand-sub{ margin:0;color:var(--text-low);font-size:0.78rem;font-family:'JetBrains Mono',monospace; }
    .pill{
        font-family:'JetBrains Mono',monospace;font-size:0.72rem;font-weight:600;
        padding:6px 12px;border-radius:30px;
        background:rgba(61,214,196,0.1); color:var(--accent); border:1px solid rgba(61,214,196,0.25);
    }
    .clock{ font-family:'JetBrains Mono',monospace;color:var(--text-mid);font-size:0.78rem; }

    /* ---- hero / animated title for Overview ---- */
    .hero-wrap{
        position:relative; text-align:center; padding:50px 20px 40px 20px;
        border:1px solid var(--line); border-radius:18px; margin-bottom:24px; overflow:hidden;
        background:linear-gradient(180deg, var(--ink-800), var(--ink-900));
    }
    .hero-glow{
        position:absolute; inset:0;
        background: radial-gradient(420px 220px at 50% 0%, rgba(61,214,196,0.18), transparent 70%);
        pointer-events:none;
        animation: pulseGlow 4s ease-in-out infinite;
    }
    @keyframes pulseGlow{
        0%,100%{ opacity:0.6; } 50%{ opacity:1; }
    }
    .hero-kicker{
        font-family:'JetBrains Mono',monospace; color:var(--accent);
        font-size:0.78rem; letter-spacing:0.25em; text-transform:uppercase;
        margin-bottom:14px; position:relative;
        animation: fadeDown 0.7s ease both;
    }
    .hero-title{
        position:relative; font-weight:900; line-height:1.08; margin:0 auto;
        max-width:920px; letter-spacing:-0.02em;
        font-size:clamp(1.6rem, 4.2vw, 3.1rem);
        background:linear-gradient(100deg, #ffffff 10%, var(--accent) 45%, var(--violet) 75%, #ffffff 100%);
        background-size:300% auto;
        -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
        animation: shimmer 6s linear infinite, popIn 0.6s cubic-bezier(.2,1.4,.4,1) both;
    }
    @keyframes shimmer{ to{ background-position: 300% center; } }
    @keyframes popIn{
        0%{ transform:scale(0.85); opacity:0; }
        60%{ transform:scale(1.04); opacity:1; }
        100%{ transform:scale(1); }
    }
    @keyframes fadeDown{
        0%{ transform:translateY(-10px); opacity:0; } 100%{ transform:translateY(0); opacity:1; }
    }
    .hero-sub{
        position:relative; color:var(--text-mid); font-size:0.98rem; margin-top:14px;
        animation: fadeUp 0.9s ease both 0.15s;
    }
    @keyframes fadeUp{
        0%{ transform:translateY(10px); opacity:0; } 100%{ transform:translateY(0); opacity:1; }
    }
    .hero-tags{ position:relative; display:flex; gap:10px; justify-content:center; margin-top:20px; flex-wrap:wrap; }
    .hero-tag{
        font-family:'JetBrains Mono',monospace; font-size:0.72rem; font-weight:600;
        padding:6px 14px; border-radius:30px; color:var(--text-hi);
        background:var(--ink-700); border:1px solid var(--line);
        animation: floaty 3.5s ease-in-out infinite;
    }
    .hero-tag:nth-child(2){ animation-delay:0.3s; }
    .hero-tag:nth-child(3){ animation-delay:0.6s; }
    .hero-tag:nth-child(4){ animation-delay:0.9s; }
    @keyframes floaty{ 0%,100%{ transform:translateY(0);} 50%{ transform:translateY(-4px);} }

    /* ---- generic surface card ---- */
    .card{ background:var(--ink-800); border:1px solid var(--line); border-radius:var(--radius); padding:20px 22px; }
    .card-tight{ padding:14px 16px; }
    .section-eyebrow{
        font-family:'JetBrains Mono',monospace; color:var(--accent); font-size:0.72rem; font-weight:600;
        letter-spacing:0.08em; text-transform:uppercase; margin-bottom:2px;
    }
    .section-title{ color:var(--text-hi); font-size:1.18rem; font-weight:700; margin:0 0 4px 0; }
    .section-desc{ color:var(--text-mid); font-size:0.88rem; margin-bottom:14px; }

    /* ---- metrics ---- */
    div[data-testid="stMetric"]{ background:var(--ink-800); border:1px solid var(--line); border-radius:var(--radius); padding:16px 18px 12px 18px; }
    div[data-testid="stMetricLabel"]{ color:var(--text-mid) !important; font-size:0.78rem !important; }
    div[data-testid="stMetricValue"]{
        font-size:1.7rem !important; font-weight:700 !important; color:var(--text-hi) !important;
        font-family:'JetBrains Mono',monospace;
    }

    /* ---- risk badge / factors ---- */
    .risk-badge{
        text-align:center; padding:11px; border-radius:10px; font-weight:700; font-size:1.0rem;
        letter-spacing:0.04em; font-family:'JetBrains Mono',monospace; margin-bottom:18px; border:1px solid;
    }
    .risk-low{ background:rgba(61,214,196,0.08); color:var(--accent); border-color:rgba(61,214,196,0.3);}
    .risk-medium{ background:rgba(245,184,78,0.1); color:var(--warn); border-color:rgba(245,184,78,0.3);}
    .risk-high{ background:rgba(239,93,111,0.1); color:var(--danger); border-color:rgba(239,93,111,0.35);}
    .factor-row{ display:flex; gap:10px; padding:9px 0; border-bottom:1px solid var(--line); font-size:0.85rem; color:var(--text-mid); }
    .factor-row:last-child{ border-bottom:none; }
    .factor-idx{ font-family:'JetBrains Mono',monospace; color:var(--accent); font-weight:700; flex-shrink:0; width:18px; }

    /* ---- buttons / inputs ---- */
    .stButton > button{
        background:linear-gradient(135deg, var(--accent), var(--accent-dim));
        color:#06231f; border:none; font-weight:700; border-radius:9px; padding:0.55rem 1rem;
    }
    .stButton > button:hover{ filter:brightness(1.08); color:#06231f; }
    .stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div{
        background:var(--ink-700) !important; border:1px solid var(--line) !important;
        color:var(--text-hi) !important; border-radius:8px !important;
    }
    .nav-label{ font-family:'JetBrains Mono',monospace; color:var(--text-low); font-size:0.7rem; letter-spacing:0.1em; text-transform:uppercase; margin:6px 0 8px 4px; }
    .footer-note{ text-align:center; color:var(--text-low); font-size:0.72rem; font-family:'JetBrains Mono',monospace; margin-top:28px; }
    hr{ border-color:var(--line) !important; }

    /* ---- AI analyst dock (present on every tab) ---- */
    .analyst-head{
        display:flex; align-items:center; gap:10px; margin-bottom:2px;
    }
    .analyst-avatar{
        width:30px;height:30px;border-radius:8px; flex-shrink:0;
        background:linear-gradient(135deg, var(--violet), var(--accent));
        display:flex;align-items:center;justify-content:center; font-size:0.85rem;
    }
    .analyst-pulse{
        width:7px;height:7px;border-radius:50%; background:var(--accent); display:inline-block;
        box-shadow:0 0 0 0 rgba(61,214,196,0.6); animation:pulseDot 1.8s infinite;
    }
    @keyframes pulseDot{
        0%{ box-shadow:0 0 0 0 rgba(61,214,196,0.55);}
        70%{ box-shadow:0 0 0 8px rgba(61,214,196,0);}
        100%{ box-shadow:0 0 0 0 rgba(61,214,196,0);}
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# DEMO MODEL — trained once and cached
# ==========================================================
@st.cache_resource
def build_demo_model():
    transaction_types = ["ATM", "POS", "Online", "QR"]
    merchant_categories = ["Food", "Travel", "Electronics", "Grocery"]
    countries = ["US", "UK", "FR", "NG", "TR"]

    base_cols = ["amount", "hour", "device_risk_score", "ip_risk_score"]
    tt_cols   = [f"transaction_type_{t}" for t in transaction_types]
    mc_cols   = [f"merchant_category_{m}" for m in merchant_categories]
    co_cols   = [f"country_{c}" for c in countries]
    feat_cols = base_cols + tt_cols + mc_cols + co_cols

    rng = np.random.default_rng(42)
    n   = 2000
    X   = pd.DataFrame(0, index=range(n), columns=feat_cols)

    X["amount"]            = rng.exponential(scale=500, size=n)
    X["hour"]              = rng.integers(0, 24, size=n)
    X["device_risk_score"] = rng.uniform(0, 1, size=n)
    X["ip_risk_score"]     = rng.uniform(0, 1, size=n)

    for col in tt_cols:
        X[col] = (rng.choice(tt_cols, size=n) == col).astype(int)
    for col in mc_cols:
        X[col] = (rng.choice(mc_cols, size=n) == col).astype(int)
    for col in co_cols:
        X[col] = (rng.choice(co_cols, size=n) == col).astype(int)

    fraud_prob = (
        0.4 * X["device_risk_score"]
        + 0.4 * X["ip_risk_score"]
        + 0.1 * (X["amount"] > 1000).astype(float)
        + 0.1 * ((X["hour"] < 6) | (X["hour"] > 22)).astype(float)
    )
    y = (rng.uniform(size=n) < fraud_prob).astype(int)

    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)
    return clf, feat_cols

model, feature_names = build_demo_model()

# ==========================================================
# SESSION STATE
# ==========================================================
defaults = {
    "risk_score": 15,
    "risk_level": "LOW",
    "risk_factors": [
        "Device fingerprint verified — matches typical user device profile.",
        "IP routing verification shows a stable geolocation footprint."
    ],
    "scan_count": 148930,
    "flag_count": 42,
    # one chat thread per module, so the analyst has context-relevant history everywhere
    "chat_overview": [{"role": "assistant", "content": "Hi — I'm watching platform-wide telemetry. Ask me about today's incident volume or flagged vectors."}],
    "chat_txn":      [{"role": "assistant", "content": "Ask me to explain the transaction scoring model or the last prediction."}],
    "chat_qr":       [{"role": "assistant", "content": "Ask me about QR payload risks or shortener red flags."}],
    "chat_site":     [{"role": "assistant", "content": "Ask me about domain reputation signals or typo-squatting patterns."}],
    "chat_upi":      [{"role": "assistant", "content": "Ask me about UPI/VPA spam signals or mule-account indicators."}],
    "chat_network":  [{"role": "assistant", "content": "Ask me to walk through the fraud network graph and likely exit paths."}],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def update_risk_profile(score, level, factors):
    st.session_state.risk_score = score
    st.session_state.risk_level = level
    st.session_state.risk_factors = factors

def render_ai_analyst(chat_key, placeholder, context_line):
    """Renders a persistent AI Analyst dock — used identically on every tab."""
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🧠  AI Analyst — ask about this module", expanded=False):
        st.markdown(f"""
        <div class="analyst-head">
            <div class="analyst-avatar">🤖</div>
            <div>
                <div style="color:var(--text-hi); font-weight:700; font-size:0.88rem;">Sentinel Analyst <span class="analyst-pulse"></span></div>
                <div style="color:var(--text-low); font-size:0.74rem; font-family:'JetBrains Mono',monospace;">{context_line}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        for chat in st.session_state[chat_key]:
            with st.chat_message(chat["role"]):
                st.write(chat["content"])

        user_input = st.chat_input(placeholder, key=f"input_{chat_key}")
        if user_input:
            st.session_state[chat_key].append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            with st.spinner("Analyzing..."):
                time.sleep(0.5)
            ai_response = (
                f"Based on the current risk profile (score {st.session_state.risk_score}%, "
                f"level {st.session_state.risk_level}), here's what stands out: "
                f"{' '.join(st.session_state.risk_factors)} "
                f"In the context of this module, I'd recommend cross-checking the flagged "
                f"attributes against your historical baseline before taking action."
            )
            st.session_state[chat_key].append({"role": "assistant", "content": ai_response})
            with st.chat_message("assistant"):
                st.write(ai_response)

# ==========================================================
# TOP BAR
# ==========================================================
st.markdown(f"""
<div class="topbar">
    <div style="display:flex; align-items:center; gap:14px;">
        <div class="brand-mark">S</div>
        <div>
            <p class="brand-name">SENTINEL</p>
            <p class="brand-sub">AI FRAUD INTELLIGENCE PLATFORM</p>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:14px;">
        <span class="clock">{datetime.now().strftime('%a %d %b · %H:%M')}</span>
        <span class="pill">● ENGINE ONLINE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.markdown('<p class="nav-label">Modules</p>', unsafe_allow_html=True)
menu_option = st.sidebar.radio(
    "Select module",
    [
        "Overview",
        "Transaction Risk Scoring",
        "QR Code Inspection",
        "Website Reputation Check",
        "UPI / VPA Lookup",
        "Network Analysis",
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown('<p class="nav-label">System</p>', unsafe_allow_html=True)
st.sidebar.markdown("""
<div class="card card-tight" style="margin-bottom:10px;">
    <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:#9aa7bd;">
        <span>Model engine</span><span style="color:#eef2f8; font-family:'JetBrains Mono',monospace;">v2.5-rf</span>
    </div>
    <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:#9aa7bd; margin-top:6px;">
        <span>AI analyst</span><span style="color:#3dd6c4; font-family:'JetBrains Mono',monospace;">on every tab</span>
    </div>
</div>
""", unsafe_allow_html=True)
st.sidebar.caption("This is a demo interface backed by a synthetically-trained model — not connected to live transaction data.")

# ==========================================================
# MAIN LAYOUT
# ==========================================================
main_col, right_col = st.columns([1.8, 1], gap="medium")

with main_col:

    # ---------------- Overview ----------------
    if menu_option == "Overview":
        st.markdown("""
        <div class="hero-wrap">
            <div class="hero-glow"></div>
            <div class="hero-kicker">◆ Welcome to Sentinel ◆</div>
            <h1 class="hero-title">AI&#8209;Powered Financial<br/>Fraud Detection</h1>
            <p class="hero-sub">Real-time transaction scoring, QR &amp; URL forensics, UPI reputation checks, and network tracing — backed by an AI analyst on every screen.</p>
            <div class="hero-tags">
                <span class="hero-tag">🧠 AI Analyst Everywhere</span>
                <span class="hero-tag">⚡ 48ms Inference</span>
                <span class="hero-tag">🛰️ Live Risk Radar</span>
                <span class="hero-tag">🕸️ Network Tracing</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Transactions scanned", f"{st.session_state.scan_count:,}", "+14% vs yesterday")
        m2.metric("Anomalies flagged", st.session_state.flag_count, "2.1% of volume")
        m3.metric("Avg. inference latency", "48 ms", "p95 pipeline")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-title" style="font-size:1.02rem;">Recent incidents</p>', unsafe_allow_html=True)

        incidents = pd.DataFrame([
            {"Time": "14:24:02", "Vector": "UPI ID anomaly",     "Target": "rewards-refund@paytm",            "Risk": 84, "Action": "Auto-hold"},
            {"Time": "14:21:15", "Vector": "Transaction",        "Target": "ACC-99812",                       "Risk": 24, "Action": "Approved"},
            {"Time": "14:15:33", "Vector": "Fraud domain",       "Target": "bank-verification-ssl.com",       "Risk": 96, "Action": "Blacklisted"},
            {"Time": "14:02:49", "Vector": "QR exploitation",    "Target": "Mule VPA redirect",               "Risk": 71, "Action": "User alerted"},
        ])
        st.dataframe(
            incidents, use_container_width=True, hide_index=True,
            column_config={"Risk": st.column_config.ProgressColumn("Risk", min_value=0, max_value=100, format="%d%%")},
        )

        render_ai_analyst("chat_overview", "Ask about platform-wide activity...", "context: platform overview")

    # ---------------- Transaction Risk Scoring ----------------
    elif menu_option == "Transaction Risk Scoring":
        st.markdown('<p class="section-eyebrow">Module 01</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-title">Transaction Risk Scoring</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Score a single transaction in real time using the trained ensemble model.</p>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            amount = st.number_input("Amount (₹)", min_value=0.0, value=500.0, step=50.0)
            transaction_type = st.selectbox("Transaction type", ["ATM", "POS", "Online", "QR"])
            merchant_category = st.selectbox("Merchant category", ["Food", "Travel", "Electronics", "Grocery"])
        with c2:
            country = st.selectbox("Country", ["US", "UK", "FR", "NG", "TR"])
            hour = st.slider("Transaction hour (24h)", 0, 23, 12)
            risk_profile = st.selectbox("Simulated risk profile", ["Low Risk", "Medium Risk", "High Risk"])

        risk_map = {"Low Risk": (0.15, 0.10), "Medium Risk": (0.50, 0.45), "High Risk": (0.95, 0.90)}
        device_risk_score, ip_risk_score = risk_map[risk_profile]

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Run fraud prediction", use_container_width=True):
            with st.spinner("Running inference pipeline..."):
                time.sleep(0.5)

            input_data = {col: 0 for col in feature_names}
            input_data["amount"]            = amount
            input_data["hour"]              = hour
            input_data["device_risk_score"] = device_risk_score
            input_data["ip_risk_score"]     = ip_risk_score
            for col_key in [f"transaction_type_{transaction_type}", f"merchant_category_{merchant_category}", f"country_{country}"]:
                if col_key in input_data:
                    input_data[col_key] = 1

            input_df    = pd.DataFrame([input_data])
            prediction  = model.predict(input_df)[0]
            probability = model.predict_proba(input_df)[0][1]
            score_pct   = int(probability * 100)

            if prediction == 1:
                current_level = "HIGH" if score_pct >= 70 else "MEDIUM"
                st.error(f"Fraud signal detected — probability **{probability:.1%}**")
                update_risk_profile(score_pct, current_level, [
                    f"Device risk score elevated at {device_risk_score:.2f}.",
                    f"IP risk score elevated at {ip_risk_score:.2f}.",
                    f"₹{amount:.0f} via {transaction_type} flagged at hour {hour}.",
                    f"Country '{country}' / category '{merchant_category}' combination is unusual.",
                ])
            else:
                st.success(f"Transaction looks legitimate — fraud probability **{probability:.1%}**")
                update_risk_profile(score_pct, "LOW", [
                    f"Device fingerprint verified (score {device_risk_score:.2f}).",
                    f"IP routing looks clean (score {ip_risk_score:.2f}).",
                    f"₹{amount:.0f} via {transaction_type} is within normal range.",
                    f"Country '{country}' / category '{merchant_category}' carries no anomaly flags.",
                ])

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<p class="section-title" style="font-size:1rem;">Model feature contributions</p>', unsafe_allow_html=True)
            importances = model.feature_importances_
            top_idx   = np.argsort(importances)[::-1][:6]
            top_feats = [feature_names[i] for i in top_idx]
            top_vals  = [importances[i] for i in top_idx]
            fig_bar = go.Figure(go.Bar(x=top_vals[::-1], y=top_feats[::-1], orientation="h", marker_color="#3dd6c4"))
            fig_bar.update_layout(
                height=230, margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9aa7bd", family="Inter"),
                xaxis=dict(gridcolor="#243044", title="Importance"), yaxis=dict(gridcolor="#243044"),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        render_ai_analyst("chat_txn", "Ask about this transaction's score...", "context: transaction risk scoring")

    # ---------------- QR Code Inspection ----------------
    elif menu_option == "QR Code Inspection":
        st.markdown('<p class="section-eyebrow">Module 02</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-title">QR Code Inspection</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Scan embedded payloads for redirect chains, shorteners, and spoofed banking keywords.</p>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload QR code image", type=["png", "jpg", "jpeg"])
        raw_qr_data   = st.text_input("Or paste a raw extracted QR payload string")

        if uploaded_file or raw_qr_data:
            with st.spinner("Extracting embedded metadata..."):
                time.sleep(0.6)
            payload = raw_qr_data if raw_qr_data else "https://shorturl.at/xK98a-secure-verification"
            if any(k in payload for k in ["shorturl", "secure-verification", "bit.ly"]):
                update_risk_profile(76, "HIGH", [
                    "Embedded URL routes through an untrusted domain shortener.",
                    "Payload contains banking keywords masquerading as a target VPA.",
                ])
                st.error("Malicious QR payload indicator triggered.")
            else:
                update_risk_profile(18, "LOW", ["QR string maps directly to a verified merchant gateway."])
                st.success("QR signature looks secure.")

        render_ai_analyst("chat_qr", "Ask about QR payload risks...", "context: QR code inspection")

    # ---------------- Website Reputation Check ----------------
    elif menu_option == "Website Reputation Check":
        st.markdown('<p class="section-eyebrow">Module 03</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-title">Website Reputation Check</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Evaluate domain age, hosting signals, and spelling-vector typo-squatting patterns.</p>', unsafe_allow_html=True)

        target_domain = st.text_input("Target domain URL", placeholder="http://login-verification-paypal-security.com")

        if st.button("Run domain audit"):
            if not target_domain:
                st.info("Enter a domain URL to run the audit.")
            else:
                with st.spinner("Scanning DNS, WHOIS, and certificate trails..."):
                    time.sleep(0.8)
                suspicious_keywords = ["secure", "bank", "login", "verification", "update", "paypal", "support"]
                found_flags = [kw for kw in suspicious_keywords if kw in target_domain.lower()]
                if len(found_flags) >= 2 or ".net" in target_domain or ".xyz" in target_domain:
                    update_risk_profile(91, "HIGH", [
                        f"Domain matches multiple typo-squatting keyphrases: {', '.join(found_flags) if found_flags else 'n/a'}.",
                        "SSL certificate authority is unrecognized or missing.",
                        "Domain was registered within the last 72 hours.",
                    ])
                    st.error("Phishing target vector verified.")
                else:
                    update_risk_profile(11, "LOW", [
                        "Domain registered with a recognized, high-trust authority.",
                        "Domain history exceeds 1,200 days.",
                    ])
                    st.success("Domain verified clean.")

        render_ai_analyst("chat_site", "Ask about this domain's reputation...", "context: website reputation check")

    # ---------------- UPI / VPA Lookup ----------------
    elif menu_option == "UPI / VPA Lookup":
        st.markdown('<p class="section-eyebrow">Module 04</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-title">UPI / VPA Lookup</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Check a virtual payment address against spam reports and reversal-rate anomalies.</p>', unsafe_allow_html=True)

        target_vpa = st.text_input("UPI handle / VPA", placeholder="e.g. trust-claims@freecharge")

        if st.button("Evaluate UPI address"):
            if not target_vpa:
                st.info("Enter a VPA to check its reputation.")
            else:
                with st.spinner("Querying historical spam databases..."):
                    time.sleep(0.5)
                if any(k in target_vpa.lower() for k in ["free", "spam", "cash"]):
                    update_risk_profile(69, "MEDIUM", [
                        "Handle reported across multiple independent spam-flag groups.",
                        "VPA shows high-frequency refund-attempt anomalies.",
                        "Associated bank account carries a mule-registration flag.",
                    ])
                    st.warning("Spammed UPI destination found — hold recommended.")
                else:
                    update_risk_profile(9, "LOW", [
                        "Fully verified KYC account ownership.",
                        "UPI velocity is within standard local brackets.",
                    ])
                    st.success("Account verified as safe.")

        render_ai_analyst("chat_upi", "Ask about this UPI handle...", "context: UPI / VPA lookup")

    # ---------------- Network Analysis ----------------
    elif menu_option == "Network Analysis":
        st.markdown('<p class="section-eyebrow">Module 05</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-title">Fraud Network Analysis</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-desc">Graph of connected entities, mule accounts, and exit pathways for the target transaction.</p>', unsafe_allow_html=True)

        st.graphviz_chart('''
        digraph {
            bgcolor="transparent";
            node [style=filled, shape=box, fontname="Helvetica", fontsize=10, fontcolor="#0a0e16"];
            edge [fontname="Helvetica", fontsize=9, color="#5e6b82", fontcolor="#9aa7bd"];
            "Target Transaction" [fillcolor="#ef5d6f", label="Suspicious Transaction\\n(Score: 84%)"];
            "Mule Wallet Alpha"  [fillcolor="#f5b84e", label="Mule Wallet Alpha\\n(Flagged IP)"];
            "Trusted Merchant"   [fillcolor="#3dd6c4", label="Trusted Portal\\n(Verified KYC)"];
            "Offshore Mixer"     [fillcolor="#ef5d6f", label="Offshore Mixer\\n(Blacklisted Address)"];
            "Target Transaction" -> "Mule Wallet Alpha" [label="rapid split-layering"];
            "Target Transaction" -> "Trusted Merchant"  [label="valid check"];
            "Mule Wallet Alpha"  -> "Offshore Mixer"    [color="#ef5d6f", style=bold, label="exfiltration pathway"];
        }
        ''')

        update_risk_profile(84, "HIGH", [
            "High proximity to documented offshore mixer addresses.",
            "Split-layering structure matches known exfiltration strategies.",
        ])
        st.info("Review the graph above to trace layering strategy and likely exit accounts.")

        render_ai_analyst("chat_network", "Ask about this network graph...", "context: network analysis")

# ==========================================================
# RIGHT PANEL — RISK RADAR (persistent across all tabs)
# ==========================================================
with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="section-eyebrow">Live</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-title" style="font-size:1.05rem;">Risk Radar</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Updates automatically as you interact with each module.</p>', unsafe_allow_html=True)

    bar_color = {"LOW": "#3dd6c4", "MEDIUM": "#f5b84e", "HIGH": "#ef5d6f"}[st.session_state.risk_level]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=st.session_state.risk_score,
        number={"suffix": "%", "font": {"color": "#eef2f8", "size": 32, "family": "JetBrains Mono"}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#5e6b82", 'tickfont': {'color': '#5e6b82', 'size': 9}},
            'bar': {'color': bar_color, 'thickness': 0.28},
            'bgcolor': "#161d2b", 'borderwidth': 1, 'bordercolor': "#243044",
            'steps': [
                {'range': [0, 35],  'color': 'rgba(61,214,196,0.08)'},
                {'range': [35, 70], 'color': 'rgba(245,184,78,0.08)'},
                {'range': [70, 100],'color': 'rgba(239,93,111,0.1)'},
            ],
        }
    ))
    fig.update_layout(height=210, margin=dict(l=15, r=15, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    badge_class = {"LOW": "risk-low", "MEDIUM": "risk-medium", "HIGH": "risk-high"}[st.session_state.risk_level]
    st.markdown(f'<div class="risk-badge {badge_class}">RISK LEVEL — {st.session_state.risk_level}</div>', unsafe_allow_html=True)

    st.markdown('<p style="color:#9aa7bd; font-size:0.78rem; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; margin-bottom:4px;">Threat factors</p>', unsafe_allow_html=True)
    factors_html = "".join(
        f'<div class="factor-row"><span class="factor-idx">{i:02d}</span><span>{f}</span></div>'
        for i, f in enumerate(st.session_state.risk_factors, 1)
    )
    st.markdown(factors_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<p class="footer-note">SENTINEL · DEMO BUILD — synthetic model, no live data connection</p>', unsafe_allow_html=True)

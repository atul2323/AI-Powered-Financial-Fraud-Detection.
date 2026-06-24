import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    precision_recall_curve,
)

st.set_page_config(
    page_title="Bank Transaction Fraud Analytics",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = "bank_transaction_risk_dataset_10000.csv"
MODEL_PATH = "bank_transaction_rf_model.pkl"
ENCODER_TRANSACTION = "transaction_encoder.pkl"
ENCODER_MERCHANT = "merchant_encoder.pkl"
ENCODER_COUNTRY = "country_encoder.pkl"

REQUIRED_COLUMNS = [
    "transaction_id",
    "user_id",
    "amount",
    "transaction",
    "merchant",
    "country",
    "hour",
    "device_risk",
    "ip_risk_score",
    "is_fraud",
]

FEATURE_COLUMNS = [
    "transaction_id",
    "user_id",
    "amount",
    "transaction",
    "merchant",
    "country",
    "hour",
    "device_risk",
    "ip_risk_score",
]

st.markdown("""
<style>
.metric-card {
    padding: 1rem;
    border-radius: 14px;
    border: 1px solid #eeeeee;
    background: #ffffff;
}
.small-text {font-size: 0.9rem; color: #666666;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    elif os.path.exists(DATA_PATH):
        data = pd.read_csv(DATA_PATH)
    else:
        st.error("Dataset not found. Upload bank_transaction_risk_dataset_10000.csv from the sidebar.")
        st.stop()

    missing = [col for col in REQUIRED_COLUMNS if col not in data.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        st.stop()

    data = data.drop_duplicates().copy()
    return data

@st.cache_data
def encode_data(df):
    encoded = df.copy()
    encoders = {}

    for col in ["transaction", "merchant", "country"]:
        encoder = LabelEncoder()
        encoded[col] = encoder.fit_transform(encoded[col].astype(str))
        encoders[col] = encoder

    return encoded, encoders

@st.cache_resource
def train_model(encoded_df):
    X = encoded_df.drop("is_fraud", axis=1)
    y = encoded_df["is_fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, zero_division=0),
        "Recall": recall_score(y_test, y_pred, zero_division=0),
        "F1 Score": f1_score(y_test, y_pred, zero_division=0),
        "ROC AUC": roc_auc_score(y_test, y_prob),
    }

    return model, X_train, X_test, y_train, y_test, y_pred, y_prob, metrics

def risk_level(score):
    if score >= 0.80:
        return "High Risk"
    if score >= 0.50:
        return "Medium Risk"
    return "Low Risk"

def add_predictions(df_original, encoded_df, model):
    result = df_original.copy()
    X = encoded_df[FEATURE_COLUMNS]
    result["fraud_probability"] = model.predict_proba(X)[:, 1]
    result["risk_score"] = (result["fraud_probability"] * 100).round(2)
    result["risk_level"] = result["fraud_probability"].apply(risk_level)
    return result

def kpi_card(label, value):
    st.metric(label, value)

def filter_data(df):
    st.sidebar.header("Filters")

    countries = sorted(df["country"].astype(str).unique())
    merchants = sorted(df["merchant"].astype(str).unique())
    transactions = sorted(df["transaction"].astype(str).unique())
    risks = ["Low Risk", "Medium Risk", "High Risk"]

    selected_countries = st.sidebar.multiselect("Country", countries, default=countries)
    selected_merchants = st.sidebar.multiselect("Merchant", merchants, default=merchants)
    selected_transactions = st.sidebar.multiselect("Transaction Type", transactions, default=transactions)
    selected_risks = st.sidebar.multiselect("Risk Level", risks, default=risks)

    min_amount, max_amount = float(df["amount"].min()), float(df["amount"].max())
    amount_range = st.sidebar.slider(
        "Amount Range",
        min_value=min_amount,
        max_value=max_amount,
        value=(min_amount, max_amount),
    )

    filtered = df[
        df["country"].astype(str).isin(selected_countries)
        & df["merchant"].astype(str).isin(selected_merchants)
        & df["transaction"].astype(str).isin(selected_transactions)
        & df["risk_level"].isin(selected_risks)
        & df["amount"].between(amount_range[0], amount_range[1])
    ]
    return filtered

uploaded_file = st.sidebar.file_uploader("Upload transaction CSV", type=["csv"])
raw_df = load_data(uploaded_file)
encoded_df, encoders = encode_data(raw_df)
model, X_train, X_test, y_train, y_test, y_pred, y_prob, metrics = train_model(encoded_df)
df = add_predictions(raw_df, encoded_df, model)

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "Fraud Analysis",
        "Model Performance",
        "Risk Monitoring",
        "Predict Transaction",
        "Investor View",
    ],
)

st.title("Bank Transaction Fraud Analytics Dashboard")
st.caption("Random Forest fraud detection dashboard based on the Bank Transaction Risk Score project")

filtered_df = filter_data(df)

if page == "Executive Dashboard":
    total_transactions = len(filtered_df)
    fraud_transactions = int(filtered_df["is_fraud"].sum())
    fraud_rate = (fraud_transactions / total_transactions * 100) if total_transactions else 0
    total_amount = filtered_df["amount"].sum()
    fraud_amount = filtered_df.loc[filtered_df["is_fraud"] == 1, "amount"].sum()
    avg_risk = filtered_df["risk_score"].mean() if total_transactions else 0

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        kpi_card("Transactions", f"{total_transactions:,}")
    with col2:
        kpi_card("Fraud Cases", f"{fraud_transactions:,}")
    with col3:
        kpi_card("Fraud Rate", f"{fraud_rate:.2f}%")
    with col4:
        kpi_card("Total Amount", f"${total_amount:,.0f}")
    with col5:
        kpi_card("Fraud Amount", f"${fraud_amount:,.0f}")
    with col6:
        kpi_card("Avg Risk Score", f"{avg_risk:.2f}%")

    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(
            filtered_df,
            names="risk_level",
            title="Transactions by Risk Level",
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fraud_by_country = filtered_df.groupby("country", as_index=False)["is_fraud"].sum()
        fig = px.bar(
            fraud_by_country,
            x="country",
            y="is_fraud",
            title="Fraud Cases by Country",
        )
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig = px.histogram(
            filtered_df,
            x="amount",
            color="is_fraud",
            nbins=40,
            title="Transaction Amount Distribution",
        )
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        fraud_by_hour = filtered_df.groupby("hour", as_index=False)["is_fraud"].sum()
        fig = px.line(
            fraud_by_hour,
            x="hour",
            y="is_fraud",
            markers=True,
            title="Fraud Cases by Hour",
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "Fraud Analysis":
    st.subheader("Fraud Pattern Analysis")

    c1, c2 = st.columns(2)
    with c1:
        fraud_by_type = filtered_df.groupby("transaction", as_index=False)["is_fraud"].sum()
        fig = px.bar(fraud_by_type, x="transaction", y="is_fraud", title="Fraud by Transaction Type")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fraud_by_merchant = filtered_df.groupby("merchant", as_index=False)["is_fraud"].sum()
        fig = px.bar(fraud_by_merchant, x="merchant", y="is_fraud", title="Fraud by Merchant")
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig = px.box(filtered_df, x="is_fraud", y="amount", title="Amount by Fraud Status")
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        fig = px.scatter(
            filtered_df,
            x="device_risk",
            y="ip_risk_score",
            color="risk_level",
            size="amount",
            hover_data=["transaction_id", "country", "merchant"],
            title="Device Risk vs IP Risk Score",
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "Model Performance":
    st.subheader("Model Performance")

    c1, c2, c3, c4, c5 = st.columns(5)
    metric_items = list(metrics.items())
    for col, (name, value) in zip([c1, c2, c3, c4, c5], metric_items):
        with col:
            kpi_card(name, f"{value:.4f}")

    c1, c2 = st.columns(2)
    with c1:
        cm = confusion_matrix(y_test, y_pred)
        fig = px.imshow(
            cm,
            text_auto=True,
            labels=dict(x="Predicted", y="Actual", color="Count"),
            x=["Non-Fraud", "Fraud"],
            y=["Non-Fraud", "Fraud"],
            title="Confusion Matrix",
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name="ROC Curve"))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Baseline"))
        fig.update_layout(title="ROC Curve", xaxis_title="False Positive Rate", yaxis_title="True Positive Rate")
        st.plotly_chart(fig, use_container_width=True)

    precision, recall, _ = precision_recall_curve(y_test, y_prob)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recall, y=precision, mode="lines", name="Precision-Recall"))
    fig.update_layout(title="Precision-Recall Curve", xaxis_title="Recall", yaxis_title="Precision")
    st.plotly_chart(fig, use_container_width=True)

    st.text("Classification Report")
    st.code(classification_report(y_test, y_pred), language="text")

elif page == "Risk Monitoring":
    st.subheader("Transaction Monitoring Center")

    high_risk = filtered_df[filtered_df["risk_level"] == "High Risk"]
    medium_risk = filtered_df[filtered_df["risk_level"] == "Medium Risk"]
    low_risk = filtered_df[filtered_df["risk_level"] == "Low Risk"]

    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_card("High Risk", f"{len(high_risk):,}")
    with col2:
        kpi_card("Medium Risk", f"{len(medium_risk):,}")
    with col3:
        kpi_card("Low Risk", f"{len(low_risk):,}")

    fig = px.histogram(filtered_df, x="risk_score", nbins=40, title="Risk Score Distribution")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Transactions for Analyst Review")
    review_df = filtered_df.sort_values("risk_score", ascending=False)[
        [
            "transaction_id",
            "user_id",
            "amount",
            "transaction",
            "merchant",
            "country",
            "hour",
            "device_risk",
            "ip_risk_score",
            "risk_score",
            "risk_level",
            "is_fraud",
        ]
    ]
    st.dataframe(review_df, use_container_width=True, hide_index=True)

elif page == "Predict Transaction":
    st.subheader("Real-Time Fraud Detection")

    c1, c2, c3 = st.columns(3)
    with c1:
        transaction_id = st.number_input("Transaction ID", min_value=1, value=1234)
        user_id = st.number_input("User ID", min_value=1, value=555)
        amount = st.number_input("Amount", min_value=0.0, value=25000.0)
    with c2:
        transaction = st.selectbox("Transaction Type", sorted(raw_df["transaction"].astype(str).unique()))
        merchant = st.selectbox("Merchant", sorted(raw_df["merchant"].astype(str).unique()))
        country = st.selectbox("Country", sorted(raw_df["country"].astype(str).unique()))
    with c3:
        hour = st.slider("Hour", 0, 23, 23)
        device_risk = st.slider("Device Risk", 0.0, 1.0, 0.92)
        ip_risk_score = st.slider("IP Risk Score", 0.0, 1.0, 0.89)

    if st.button("Predict Fraud Risk"):
        input_df = pd.DataFrame({
            "transaction_id": [transaction_id],
            "user_id": [user_id],
            "amount": [amount],
            "transaction": [transaction],
            "merchant": [merchant],
            "country": [country],
            "hour": [hour],
            "device_risk": [device_risk],
            "ip_risk_score": [ip_risk_score],
        })

        encoded_input = input_df.copy()
        encoded_input["transaction"] = encoders["transaction"].transform(encoded_input["transaction"].astype(str))
        encoded_input["merchant"] = encoders["merchant"].transform(encoded_input["merchant"].astype(str))
        encoded_input["country"] = encoders["country"].transform(encoded_input["country"].astype(str))

        probability = model.predict_proba(encoded_input[FEATURE_COLUMNS])[0][1]
        score = probability * 100
        level = risk_level(probability)

        st.metric("Fraud Probability", f"{score:.2f}%")
        st.metric("Risk Level", level)

        if level == "High Risk":
            st.error("Recommended action: Block transaction and send to analyst review.")
        elif level == "Medium Risk":
            st.warning("Recommended action: Require extra verification.")
        else:
            st.success("Recommended action: Approve transaction.")

elif page == "Investor View":
    st.subheader("Investor-Grade Impact View")

    total_amount = filtered_df["amount"].sum()
    fraud_amount = filtered_df.loc[filtered_df["is_fraud"] == 1, "amount"].sum()
    detected_fraud_amount = filtered_df.loc[(filtered_df["is_fraud"] == 1) & (filtered_df["risk_level"].isin(["High Risk", "Medium Risk"])), "amount"].sum()
    high_risk_amount = filtered_df.loc[filtered_df["risk_level"] == "High Risk", "amount"].sum()
    detection_rate = detected_fraud_amount / fraud_amount * 100 if fraud_amount else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("Amount Processed", f"${total_amount:,.0f}")
    with col2:
        kpi_card("Confirmed Fraud Amount", f"${fraud_amount:,.0f}")
    with col3:
        kpi_card("Detected Fraud Amount", f"${detected_fraud_amount:,.0f}")
    with col4:
        kpi_card("Value Detection Rate", f"{detection_rate:.2f}%")

    impact = pd.DataFrame({
        "Metric": ["Processed Amount", "Fraud Amount", "Detected Fraud Amount", "High Risk Amount"],
        "Value": [total_amount, fraud_amount, detected_fraud_amount, high_risk_amount],
    })
    fig = px.bar(impact, x="Metric", y="Value", title="Financial Impact")
    st.plotly_chart(fig, use_container_width=True)

    importance = pd.DataFrame({
        "Feature": FEATURE_COLUMNS,
        "Importance": model.feature_importances_,
    }).sort_values("Importance", ascending=False)

    fig = px.bar(importance, x="Importance", y="Feature", orientation="h", title="Top Fraud Risk Drivers")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
### Investor Talking Points

• The dashboard converts fraud detection into measurable financial impact.  
• It shows fraud exposure, detected fraud value, risk levels, and model quality.  
• It supports analyst review through ranked transaction monitoring.  
• It includes real-time scoring for new bank transactions.  
""")

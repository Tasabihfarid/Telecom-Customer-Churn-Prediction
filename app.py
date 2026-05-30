import streamlit as st
import pandas as pd
import numpy as np
import joblib

# 1. تحميل الموديل والميزات التي تم حفظها من النوت بوك
model = joblib.load('best_churn_model.pkl')
selected_features = joblib.load('selected_features.pkl')

# 2. إعداد واجهة مستخدم احترافية وبسيطة للموقع
st.set_page_config(page_title="Customer Churn Predictor", page_icon="📊", layout="centered")

st.title("📊 Telecom Customer Churn Prediction App")
st.markdown("This application predicts whether a telecom customer is likely to churn (leave the company) based on their account details and subscribed services.")
st.write("---")

st.sidebar.header("🔧 Customer Input Features")
st.sidebar.markdown("Adjust the details below to evaluate the customer:")

# 3. بناء خانات إدخال البيانات ديناميكياً بناءً على الميزات المختارة
input_data = {}

# القوائم والخيارات المتاحة بناءً على الـ One-Hot Encoding
binary_options = ["No", "Yes"]
contract_options = ["Month-to-month", "One year", "Two year"]
internet_options = ["DSL", "Fiber optic", "No"]

# إدخال القيم الرقمية
if 'tenure' in selected_features:
    input_data['tenure'] = st.sidebar.slider("Tenure (Months)", min_value=0, max_value=72, value=12)
if 'MonthlyCharges' in selected_features:
    input_data['MonthlyCharges'] = st.sidebar.number_input("Monthly Charges ($)", min_value=0.0, max_value=150.0, value=65.0)
if 'TotalCharges' in selected_features:
    input_data['TotalCharges'] = st.sidebar.number_input("Total Charges ($)", min_value=0.0, max_value=9000.0, value=800.0)
if 'Total_Services_Subscribed' in selected_features:
    input_data['Total_Services_Subscribed'] = st.sidebar.slider("Total Services Subscribed", min_value=0, max_value=6, value=2)

# إدخال القيم النصية المشفرة (Categorical Features)
categorical_inputs = {
    'Contract_One year': ("Contract: One year", binary_options),
    'Contract_Two year': ("Contract: Two year", binary_options),
    'InternetService_Fiber optic': ("Internet Service: Fiber optic", binary_options),
    'InternetService_No': ("Internet Service: No Internet", binary_options),
    'PaymentMethod_Credit card (automatic)': ("Payment: Credit Card", binary_options),
    'PaymentMethod_Electronic check': ("Payment: Electronic Check", binary_options),
    'PaymentMethod_Mailed check': ("Payment: Mailed Check", binary_options),
    'PaperlessBilling_Yes': ("Paperless Billing", binary_options),
    'Partner_Yes': ("Has a Partner", binary_options),
    'Dependents_Yes': ("Has Dependents", binary_options),
    'TechSupport_Yes': ("Subscribed to Tech Support", binary_options),
    'OnlineSecurity_Yes': ("Subscribed to Online Security", binary_options)
}

for feat, (label, options) in categorical_inputs.items():
    if feat in selected_features:
        choice = st.sidebar.selectbox(label, options, index=0)
        input_data[feat] = 1 if choice == "Yes" else 0

# 4. معالجة البيانات المدخلة لتطابق ترتيب ميزات الموديل تماماً
features_df = pd.DataFrame([input_data])
features_df = features_df.reindex(columns=selected_features, fill_value=0)

# 5. عرض البيانات التي تم إدخالها في الصفحة الرئيسية
st.subheader("📋 Submitted Customer Profile Summary")
st.dataframe(features_df)

# 6. زر تشغيل التنبؤ وعرض النتائج
st.write("")
if st.button("🚀 Run Predictive Analysis", use_container_width=True):
    prediction = model.predict(features_df)[0]
    prediction_proba = model.predict_proba(features_df)[0][1]

    st.write("---")
    st.subheader("🔮 Model Analysis Result")

    if prediction == 1:
        st.error(f"⚠️ **High Churn Risk!** This customer is highly likely to leave the company. (Churn Probability: {prediction_proba:.2%})")
    else:
        st.success(f"✅ **Loyal Customer!** This customer is likely to stay with the company. (Churn Probability: {prediction_proba:.2%})")

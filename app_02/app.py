import streamlit as st
import pandas as pd
import joblib
from sklearn.metrics import r2_score, accuracy_score, precision_score, recall_score, f1_score

# ---- Load Models ---- #
@st.cache_resource
def load_models():
    clf_model = joblib.load("rf_product_classifier.pkl")
    reg_model = joblib.load("sales_model.pkl")
    return clf_model, reg_model

rf_product_classifier, sales_model = load_models()

st.set_page_config(page_title="Business Analyst App", layout="wide")
st.title("📊 Business Analyst App - Predict Sales & Classify Products")

if "features" not in st.session_state:
    st.session_state.features = []
if "target" not in st.session_state:
    st.session_state.target = ""
if "task" not in st.session_state:
    st.session_state.task = "Classification"
if "manual_input" not in st.session_state:
    st.session_state.manual_input = {}

uploaded_file = st.file_uploader("📁 Upload your dataset (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("🔍 Preview of Uploaded Data")
        st.dataframe(df.head())

        task = st.radio("Select Task", ["Classification", "Regression"], index=0 if st.session_state.task == "Classification" else 1)
        st.session_state.task = task

        required_features_sales = ['Country/Region', 'City', 'State', 'Category', 'Sub-Category', 'Product Name']
        required_features_classify = ['Country/Region', 'City', 'State', 'Category', 'Sub-Category', 'Sales']

        with st.form("form_features"):
            st.write("### ✨ Select Features and Target")

            if task == "Regression" and all(col in df.columns for col in required_features_sales):
                features = st.multiselect("Select input features (X)", options=df.columns, default=required_features_sales)
                st.success("✅ Recommended features selected for Sales Prediction.")
            elif task == "Classification" and all(col in df.columns for col in required_features_classify):
                features = st.multiselect("Select input features (X)", options=df.columns, default=required_features_classify)
                st.success("✅ Recommended features selected for Product Classification.")
            else:
                features = st.multiselect("Select input features (X)", options=df.columns)

            st.session_state.features = features

            target = st.selectbox("Select target column (y)", options=df.columns, index=df.columns.get_loc("Product Name") if "Product Name" in df.columns else 0)
            st.session_state.target = target

            submit = st.form_submit_button("🚀 Run Prediction")

        if submit:
            st.session_state.run_model = True
            st.rerun()

        if st.session_state.features and st.session_state.target and st.session_state.get("run_model"):
            X = df[st.session_state.features]
            y = df[st.session_state.target]

            try:
                if st.session_state.task == "Classification":
                    preds = rf_product_classifier.predict(X)
                    df["Prediction"] = preds

                    acc = accuracy_score(y, preds)
                    prec = precision_score(y, preds, average='weighted', zero_division=0)
                    rec = recall_score(y, preds, average='weighted', zero_division=0)
                    f1 = f1_score(y, preds, average='weighted', zero_division=0)

                    st.success(f"✅ Accuracy: {acc:.4f}")
                    st.success(f"✅ Precision: {prec:.4f}")
                    st.success(f"✅ Recall: {rec:.4f}")
                    st.success(f"✅ F1 Score: {f1:.4f}")
                else:
                    preds = sales_model.predict(X)
                    df["Prediction"] = preds
                    r2 = r2_score(y, preds)
                    st.success(f"✅ R² Score: {r2:.4f}")

                st.subheader("📈 Prediction Results")
                st.dataframe(df[[st.session_state.target, "Prediction"]].head(10))

                @st.cache_data
                def convert_df(df):
                    return df.to_csv(index=False).encode("utf-8")

                csv = convert_df(df)

                st.download_button(
                    label="📥 Download Predictions as CSV",
                    data=csv,
                    file_name="predicted_results.csv",
                    mime="text/csv"
                )

                st.subheader("🧮 Manual Prediction Input")
                manual_form = st.form("manual_input")
                for col in st.session_state.features:
                    default_val = st.session_state.manual_input.get(col, "")
                    st.session_state.manual_input[col] = manual_form.text_input(f"Enter {col}", value=default_val)
                manual_submit = manual_form.form_submit_button("Predict from Input")

                if manual_submit:
                    cleaned_input = {}
                    for k in st.session_state.features:
                        val = st.session_state.manual_input.get(k, "")
                        try:
                            cleaned_input[k] = float(val)
                        except:
                            cleaned_input[k] = val

                    user_df = pd.DataFrame([cleaned_input])
                    user_df = user_df[st.session_state.features]  # ensure correct column order

                    try:
                        if st.session_state.task == "Classification":
                            result = rf_product_classifier.predict(user_df)
                        else:
                            # Drop columns not seen during training if present
                            user_df = user_df[[col for col in user_df.columns if col in sales_model.feature_names_in_]]
                            result = sales_model.predict(user_df)
                        st.success(f"🔮 Predicted Value: {result[0]}")
                    except Exception as e:
                        st.error(f"❌ Prediction failed: {str(e)}")

            except Exception as e:
                st.error(f"❌ Prediction failed. Reason: {str(e)}")

    except Exception as e:
        st.error(f"❌ Failed to read file. Reason: {str(e)}")
else:
    st.info("⬆️ Please upload a CSV or Excel file to begin.")

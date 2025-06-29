# 🤖 AI Chatbot App Collection or Data Science Apps – by Muhammad Ahmad Bhutta

This repository contains a **collection of AI-powered chatbot applications**, built using **Streamlit**, **Python**, and **Gemini 2.0 Flash API**. Each app provides a modern and interactive user interface for AI conversations. I also create the apps for **Data Science**

---

## 📂 Available Apps

### ✅ `app_01`
A basic chatbot web app powered by **Gemini 2.0 Flash**. Designed to simulate a smart assistant-like experience using Streamlit.

**Core Features:**
- Integration with Gemini 2.0 Flash API
- Simple and clean Streamlit-based UI
- User and bot avatars
- Chat export to **PDF** and **TXT**
- File upload support
- Image-to-text (OCR) functionality
- API key input 

❌ Not Yet Available:
- Theme toggle (light/dark mode)
- Voice input
- Emoji reactions
- Prompt/response copy buttons
- Typing animation

📁 Folder: `app_01/`  
📄 Main file: `app.py`

### ✅ `app_02`
An interactive business analytics and sales prediction web app built with **Streamlit**, **PyCaret**, and **Scikit-learn**. Designed to help users analyze business data, predict sales, and classify product names using AI.

**Core Features:**
- Business analytics dashboard for exploring and visualizing data
- Predict sales using a pre-trained **PyCaret** regression model
- Classify product names using a **Random Forest Classifier** with hyperparameter tuning
- Evaluate model performance with metrics like **R²**, **Accuracy**, **Precision**, **Recall**, and **F1 Score**
- User-friendly Streamlit interface

**Technologies & Libraries Used:**
- **Streamlit** — for building the web app (`streamlit`)
- **Pandas** — for data manipulation (`pandas`)
- **Joblib** — for saving and loading models (`joblib`)
- **Scikit-learn (sklearn)** — for metrics and additional model training
- **PyCaret** — for automated machine learning workflows

❌ Not Yet Available:
- Real-time data connection
- In-app model retraining
- User authentication
- Advanced custom visualizations

📁 Folder: `app_02/`  
📊 Dataset folder: `datasets/`
📄 Main file: `app.py`  
📁 Pre-trained models: `pre_training_models/`  
📦 Saved sales prediction model: `sales_model.pkl`  
📦 Saved product classification model: `rf_product_classifier.pkl` I not push because it take much more memory(above 2gb).
More apps like `app_03`, `app_04`, etc. will be added soon with improved designs and extra features.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Choose an App

```bash
cd app_01
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

---

## 🔑 Gemini API Setup

1. Visit [Google AI Studio](https://makersuite.google.com/)
2. Generate your Gemini API Key
3. Paste the key into the sidebar field when running the app

---

## 📌 Project Vision

This repo is part of a long-term journey to:
- Build lightweight AI tools for education, business, and productivity
- Experiment with agent-style chatbots
- Help small businesses integrate intelligent chat systems
- Showcase backend + frontend power using Python + Gemini

---

## 📎 License

Released under the **MIT License** — feel free to use and contribute!

---

## 🌟 Author

**Muhammad Ahmad Bhutta**  
Freelance Data Scientist | AI Developer | Open to Work  
🔗 [LinkedIn](https://www.linkedin.com/in/ahmad-azhar-518231294/)  
📺 [YouTube](https://youtube.com/@bhuttageverything)

---

> ⭐ Star this repo to stay updated as more AI and Data Science apps are added!

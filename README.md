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

### ✅ `app_03`: Stock Market Forecasting App

A robust and interactive **stock price forecasting** web app built with Streamlit, Statsmodels, Plotly, and YFinance. This tool allows users to analyze, visualize, and predict stock market prices with powerful time series models.

### Core Features:
- Select stock ticker symbols (e.g., AAPL, MSFT, TSLA)
- Choose custom date ranges for historical data
- Visualize Open, Close, High, Low, and Volume data with Plotly charts
- Perform stationarity tests using ADF
- Decompose time series data into trend, seasonality, and residuals
- Build and train SARIMAX models with adjustable parameters
- Forecast future stock prices and visualize predictions vs. actuals
- User-friendly Streamlit sidebar and interactive controls

### Technologies & Libraries Used:
- **Streamlit** — for the interactive web app (`streamlit`)
- **Pandas** — for data manipulation (`pandas`)
- **YFinance** — to download stock market data (`yfinance`)
- **Statsmodels** — for time series modeling (`statsmodels`)
- **Plotly** — for dynamic visualizations (`plotly`)
- **Matplotlib & Seaborn** — for extra plots (`matplotlib`, `seaborn`)

### ❌ Not Yet Available:
- Automated model selection
- Backtesting module
- Real-time streaming data
- User authentication and profile saving

📁 **Folder:** `app_03/`  
📄 **Main file:** `app.py`  
📁 **Images:** `image/` folder for app visuals  
*More forecasting tools and asset types will be added soon!*

---

### ✅ `app_04`: Plotly Dashboard App

A lively, animated data visualization dashboard showcasing global GDP and Life Expectancy using Plotly Express and Streamlit. Designed to demonstrate interactive, multi-year insights at a glance.

### Core Features:
- Load and display Gapminder dataset for global data
- Explore summary statistics and column details
- Visualize GDP per Capita vs. Life Expectancy with bubble sizes representing population
- Animate changes over time with Play/Pause functionality
- Select custom years to focus on specific trends
- Fully responsive Plotly charts for presentation-ready visuals

### Technologies & Libraries Used:
- **Streamlit** — for building the web app (`streamlit`)
- **Pandas** — for data management (`pandas`)
- **Plotly Express** — for animated, interactive plots (`plotly.express`)

### ❌ Not Yet Available:
- Drill-down filters by country or region
- Exporting dashboards to PDF/PNG
- Advanced multi-page layouts
- Custom styling and theming options

📁 **Folder:** `app_04/`  
📊 **Dataset:** built-in Gapminder data from Plotly Express  
📄 **Main file:** `app.py`  
*More visual storytelling templates coming soon!*

---

### ✅ `app_05`: Global Data Dashboard App

A modern, minimalistic Streamlit dashboard to explore global socio-economic data by continent with clear KPIs and comparative charts.

### Core Features:
- Filter dataset by continent using a Streamlit sidebar
- See key performance indicators like **Average GDP per Capita**
- View scatter plots for GDP vs. Life Expectancy, sized by population
- Visualize population distribution by country with bar charts
- Multi-column layout for side-by-side comparison
- Clean, responsive design for easy insights

### Technologies & Libraries Used:
- **Streamlit** — for the dashboard framework (`streamlit`)
- **Pandas** — for data processing (`pandas`)
- **Plotly Express** — for dynamic charts (`plotly.express`)

### ❌ Not Yet Available:
- Year selector for time series analysis
- Download reports or CSV exports
- Advanced filters (country, region, income level)
- User account dashboards

📁 **Folder:** `app_05/`  
📊 **Dataset:** built-in Gapminder dataset from Plotly Express  
📄 **Main file:** `app.py`  

### ✅ `app_06`: US Population Migration Dashboard

A modern, interactive Streamlit dashboard to analyze US population trends and migrations by state with maps, heatmaps, donut charts, and animated 3D plots.

### Core Features:
- Filter data by **year** and **color theme** with sidebar
- Visualize **inbound & outbound migration** using donut charts
- Interactive **3D scatter plot**: Year vs Population vs Migration
- **Bubble choropleth map** for state comparison
- Detailed **heatmap** of population by state over time
- Custom **dark theme** and CSS for sleek metrics and layout

### Technologies & Libraries Used:
- **Streamlit** — app framework (`streamlit`)
- **Pandas** — data manipulation (`pandas`)
- **Altair** — heatmaps & donut charts (`altair`)
- **Plotly Express & Graph Objects** — advanced mapping & 3D (`plotly.express`, `plotly.graph_objects`)

### ❌ Not Yet Available:
- Downloadable reports or exports
- Time series forecasting
- Demographic breakdowns (age, income)
- User comments or insights

📁 **Folder:** `app_06/`  
📂 **Dataset Folder:** `datasets/`  
📊 **Dataset:** `datasets/us-population-2010-2019-reshaped.csv`  
📄 **Main file:** `app.py`  
*Stay tuned for enhanced migration insights and real-time data updates!*


---

### ✅ `app_07`: Sales Performance Dashboard

A polished Streamlit dashboard to explore supermarket sales data with multi-level charts, dynamic filters, and correlation heatmaps.

### Core Features:
- Filter by **City**, **Customer Type**, **Gender**, and **Color Theme**
- **Key KPIs**: Total Sales, Average Rating (with stars), Avg. Sales per Transaction
- Interactive **Sales by Product Line** bar chart
- **Hourly Sales Trends**: find peak hours
- **Sunburst** and **Treemap** charts for hierarchical breakdowns
- **Correlation Heatmap** for key metrics
- **Bubble Chart**: Unit Price vs Total Sales sized by Quantity
- Clean, responsive design for business insights

### Technologies & Libraries Used:
- **Streamlit** — app framework (`streamlit`)
- **Pandas** — data processing (`pandas`)
- **Plotly Express** — charts & maps (`plotly.express`)

### ❌ Not Yet Available:
- Real geo mapping with live coordinates
- Multi-year sales comparison
- Downloadable reports & chart images
- User login & saved dashboards

📁 **Folder:** `app_07/`  
📂 **Dataset Folder:** `datasets/`  
📊 **Dataset:** `datasets/supermarkt_sales.xlsx`  
📄 **Main file:** `app.py`  
*More visualizations and forecasting tools coming soon!*


*Stay tuned for new expansions with richer datasets and real-time data updates!*

---
More apps like `app_08`, `app_09`,`app_10` etc. will be added soon with improved designs and extra features.

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

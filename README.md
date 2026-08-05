# 🩺 AI Dataset Doctor

An intelligent dataset quality assessment tool built with **Python**, **Pandas**, and **Streamlit**.

AI Dataset Doctor helps Data Scientists and Machine Learning Engineers analyze the quality of CSV datasets before training machine learning models. The application automatically performs data quality checks, statistical analysis, outlier detection, and generates AI-powered recommendations for improving dataset quality.

---

# 🚀 Features

## 📊 Dataset Overview

- Number of rows and columns
- Memory usage
- Data type detection
- Numerical, categorical, boolean and datetime feature counts

---

## 🧩 Missing Values Analysis

- Total missing values
- Missing percentage
- Affected columns
- Detailed missing value table

---

## 📑 Duplicate Detection

- Duplicate row count
- Duplicate percentage
- Duplicate row preview

---

## 📈 Statistical Summary

Automatic descriptive statistics for numerical features including:

- Mean
- Median
- Standard Deviation
- Minimum
- Maximum
- Quartiles

---

## 🩺 Dataset Health Check

Automatic health assessment of the dataset.

Includes:

### Distribution Analysis

- Normal Distribution
- Moderately Right Skewed
- Highly Right Skewed
- Left Skewed

---

### Variability Analysis

Detects numerical features with:

- Low Variability
- Moderate Variability
- High Variability

---

### Balance Analysis

Checks categorical feature balance and detects class imbalance.

---

## 📌 Outlier Detection

Automatically selects the appropriate detection method.

### Normal Distribution

Uses:

- Z-Score Method

### Non-Normal Distribution

Uses:

- Interquartile Range (IQR)

Reports:

- Outlier count
- Outlier percentage
- Affected features

---

## 🤖 AI Insights

Google Gemini integration generates intelligent dataset quality reports.

The AI automatically provides:

### ⚠️ Warnings

Detects important issues such as:

- Missing values
- Duplicate records
- Distribution problems
- Outliers
- High variability
- Imbalanced categorical features

### 💡 Actionable Recommendations

Provides practical suggestions for improving dataset quality before machine learning.

---

# 🛠 Tech Stack

- Python
- Pandas
- NumPy
- Streamlit
- Google Gemini API
- python-dotenv


---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/AI-Dataset-Doctor.git
```

Go to the project

```bash
cd AI-Dataset-Doctor
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Streamlit

```bash
streamlit run app/app.py
```

---

# 🔑 Environment Variables

Create a `.env` file.

Example:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

# ⚠️ AI Insights Note

The AI Insights feature uses the Google Gemini API.

Depending on your country or network restrictions, access to the Gemini API may require a VPN.

If the AI service is unavailable, the rest of the application continues to function normally.

---

# 🎯 Project Goals

- Improve dataset quality before machine learning
- Reduce common data quality issues
- Automate exploratory dataset inspection
- Provide AI-assisted recommendations
- Demonstrate clean software architecture for data science applications

---

# 📌 Future Improvements

- PDF Report Export
- Automatic Data Cleaning
- Dataset Quality Score
- Correlation Analysis
- Feature Importance Suggestions
- Multi-LLM Support
- Offline Smart Insights Engine

---

# 👩‍💻 Author

Developed by Kimiya Jmshidi
# 🔎 Bias & Source Diversity Checker

Analyze search result bias and source diversity using the **Exa AI API**.  
This project fetches search results for a query, measures domain concentration, and performs sentiment analysis on snippets to uncover bias and diversity across sources.

---

## 🚀 Features

- Fetch search results using the Exa AI API
- Extract and analyze domains to detect dominance
- Compute diversity metrics:
  - **Herfindahl–Hirschman Index (HHI)**
  - **Shannon Entropy**
  - **Gini Coefficient**
- Perform sentiment analysis on snippets with HuggingFace Transformers
- Visualize:
  - Top domains (bar chart)
  - Domain share (pie chart)
  - Average sentiment per domain (heatmap)
- Identify potential bias and highlight diversity of perspectives

---

## 🧰 Modules / Libraries Used

- `exa_py` – Connect to Exa AI search API  
- `pandas` – Data storage and manipulation  
- `numpy` – Numerical operations  
- `transformers` – HuggingFace sentiment analysis  
- `matplotlib` & `seaborn` – Data visualization  

---

## 🏗️ Class Overview

The `BiasDiversityCheck` class contains methods to collect data, compute diversity metrics, analyze sentiment, and visualize results:

| Method | Purpose |
|--------|---------|
| `__init__` | Initialize query, target results, and Exa API connection |
| `__repr__` | Readable string representation of the object |
| `get_responses` | Fetch search results and store in a DataFrame |
| `find_dominant_domain` | Identify if a single domain dominates the results |
| `find_hhi` | Compute Herfindahl–Hirschman Index to measure concentration |
| `find_shannon_entropy` | Compute Shannon entropy for domain distribution |
| `find_gini` | Compute Gini coefficient for inequality in domain counts |
| `sentiment_analysis` | Perform sentiment analysis on snippets using HuggingFace |
| `visualize` | Generate bar chart, pie chart, and heatmap for domains and sentiment |

---

## ⚡ Usage

```python
from bias_diversity_checker import BiasDiversityCheck

# Initialize the checker
qsearch = BiasDiversityCheck(query="AI Ethics", page=10, target=50)

# Fetch search results
df = qsearch.get_responses()

# Analyze diversity
print(qsearch.find_dominant_domain())
print(qsearch.find_hhi())
print(qsearch.find_shannon_entropy())
print(qsearch.find_gini())

# Sentiment analysis
sentiment_df = qsearch.sentiment_analysis()
sentiment_df.head()

# Visualize results
qsearch.visualize()

```

## 📊 Visualizations

- Bar chart: Top 10 domains by count

- Pie chart: Share of top 10 domains

- Heatmap: Average sentiment by domain

These help quickly interpret bias and diversity in search results.

## 📌 Insights

Detect whether search results are dominated by a few sources

Measure diversity using multiple metrics (HHI, entropy, Gini)

Identify sentiment skew across domains (positive or negative bias)

Understand the global vs. local representation of sources


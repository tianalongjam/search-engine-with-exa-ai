from exa_py import Exa
import pandas as pd
import numpy as np
from transformers import pipeline
import matplotlib.pyplot as plt
import seaborn as sns

# # query = input('Search here: ')

class BiasDiversityCheck():
    def __init__(self, query = "AI Ethics", page = 10, target = 50):
            
            """
            Constructor for BiasDiversityChecker

            Args:
                query (str): Search query
                target (int): Total number of results to fetch
                page (int): Number of results per request (not more than 10)
            """
            
            self.query = query
            self.page = page
            self.target = target
            self.list = list()
            self.exa = Exa('----')
            self.df = pd.DataFrame()

    
    def __repr__(self):
        return f"The query you provided is {self.query} for {self.target} results"
        
    def get_responses(self):

        """
        Get the top n responses for the query given, stored in a dataframe
        """

        for responses in range(0,self.target,self.page):
            response = self.exa.search(
                self.query,
                num_results=self.page,
                type='keyword'        
                )

            self.list.extend(response.results)


        for r in self.list:
            new_row = pd.DataFrame([{
                        "Title": r.title,
                        "URL": r.url,
                        "Published_date": r.published_date,
                        "Author": r.author,
                        "Snippet": r.text,
                        "domain": r.url.split("/")[2] if "://" in r.url else r.url
                    }])

            self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.domain_counts = self.df["domain"].value_counts()
        self.shares = self.domain_counts/self.domain_counts.sum()
        
        return self.df      

    def find_dominant_domain(self):

        """
        Finds the largest domain solely by calculating the share % of the domain with the most results
        """

        top_dom = self.shares.max()
           
        if top_dom >= 0.5:
            return(f"{self.domain_counts.idxmax()} dominates the results that we got")
        else:
            return("No particular domain dominates your search results")
    
    def find_hhi(self):

        """
        The Herfindahl–Hirschman Index (HHI) is a measure of market concentration that can also be applied to search results. It is calculated by summing the squares of the market shares (or proportions) of all entities.
        """


        hhi = (self.shares ** 2).sum().round(2)
        
        if hhi == 1.0:
            return (f"The computed HHI for the {self.query} query is ~{hhi}, which indicates a perfect concentration distribution of sources. The {self.domain_counts.idxmax()} domain dominates the search results, suggesting a dominance in those results.")
        elif hhi == 1/len(self.domain_counts):
            return (f"perfect equality: results evenly distributed across {1/len(self.domain_counts)} domains")
        elif hhi < 0.15:
            return "The computed HHI for this query indicates an unconcentrated distribution of sources. No single domain dominates the search results, suggesting a diverse set of perspectives."
        elif 0.15 <= hhi < 0.25:
            return "The computed HHI for this query indicates a moderately concentrated distribution of sources. A handful of domains contribute most of the results, which provides some diversity, but there is noticeable imbalance in representation."
        else:
            return "The computed HHI for this query indicates a highly concentrated distribution of sources. A small number of domains dominate the results, which limits diversity and may lead to a biased or narrow perspective in the retrieved information."
        
    def find_shannon_entropy(self):

        """
        Measures inequality in domain distribution; 0 = perfectly equal, 1 = all results from one domain.
        """


        entropy = - (self.shares * np.log(self.shares)).sum()

        if 0 <= entropy < 0.3:
            return "The normalized entropy for this query falls in the low range, indicating that the results are concentrated in only a few domains. This suggests limited diversity of perspectives, with a higher risk of bias from dominant sources."
        elif 0.3 <= entropy < 0.7:
            return "The normalized entropy for this query is in the moderate range, showing that results are spread across multiple domains but still somewhat uneven. A few domains contribute more heavily, so while there is some diversity, certain perspectives are more influential than others."
        else:
            return "The normalized entropy for this query is in the high range, meaning the results are well-distributed across many domains. No single source dominates, suggesting a broad and balanced range of perspectives in the retrieved information."
    
    def find_gini(self):

        """Measures diversity/uncertainty in domain distribution; higher values indicate more evenly spread results."""

        counts = self.domain_counts.values
        sorted_counts = np.sort(counts)
        n = len(counts)
        cumulative = np.cumsum(sorted_counts) / counts.sum()
        gini = (n + 1 - 2 * np.sum(cumulative) / cumulative[-1]) / n

        if gini < 0.25:
            return "The Gini coefficient for this query falls in the low range, suggesting that the results are fairly evenly distributed across domains. No single source dominates, and the overall diversity of perspectives is strong."
        elif 0.25 <= gini <0.5:
            return "The Gini coefficient for this query lies in the moderate range, indicating that while there is some diversity, a few domains contribute more results than others. This creates a mix of perspectives, though some sources are more prominent."
        elif 0.5<= gini <1.0:
            return "The Gini coefficient for this query is in the high range, showing that the results are heavily skewed toward a small number of domains. This reduces diversity and may cause the retrieved information to reflect a narrower perspective."
        else:
            return "The Gini coefficient for this query is out of bounds"
        
    def sentiment_analysis(self):
        """
        Run sentiment analysis on the snippets (or titles if snippets are missing).
        Uses HuggingFace sentiment pipeline.
        """
        if self.df is None or self.df.empty:
            raise ValueError("No data available. Run collect_data() first.")

        sentiment_pipeline = pipeline("sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english")

        text_column = self.df["Snippet"].fillna(self.df["Title"])

        sentiments = []
        for text in text_column:
            if not text or text.strip() == "":
                sentiments.append(0.0)
                continue
            result = sentiment_pipeline(text[:512])[0]
            score = result["score"]
            score = score if result["label"] == "POSITIVE" else -score
            sentiments.append(score)

        self.df["Sentiment"] = sentiments
        return self.df[["Title", "Snippet", "Sentiment"]]
    
    def visualize(self):

        #bar graph
        plt.figure(figsize=(10, 5))
        self.domain_counts.head(10).plot(kind="bar")
        plt.title(f"Top 10 Domains for '{self.query}'")
        plt.ylabel("Count")
        plt.show()

        #pie chart
        plt.figure(figsize=(6, 6))
        self.domain_counts.head(10).plot(kind="pie", autopct='%1.1f%%')
        plt.title(f"Domain Share for '{self.query}'")
        plt.ylabel("")
        plt.show()

        #heatmap: domain vs sentiment
        sentiment_by_domain = self.df.groupby("domain")["Sentiment"].mean().reset_index()
        sentiment_pivot = sentiment_by_domain.pivot_table(index="domain", values="Sentiment")
        plt.figure(figsize=(6, len(sentiment_pivot) / 2))
        sns.heatmap(sentiment_pivot, annot=True, cmap="coolwarm", center=0)
        plt.title("Average Sentiment by Domain")
        plt.show()

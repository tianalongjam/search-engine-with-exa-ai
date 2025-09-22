from exa_py import Exa
import pandas as pd


exa = Exa('a2e035a2-d6dd-4860-9202-8df13b04f2b6')

df = pd.DataFrame()
data_dict = {}

# query = input('Search here: ')
query = "AI Ethics"

response = exa.search(
  query = "AI Ethics",
  num_results=50,
  type='keyword'
  # include_domains=['https://www.tiktok.com'],
)

page= 10
target = 50
data_list = []

for responses in range(0,target,page):
      response = exa.search(
        query,
        num_results=page,
        type='keyword'        
        )

      data_list.extend(response.results)


for r in data_list:
      new_row = pd.DataFrame([{
            "Title": r.title,
            "URL": r.url,
            "Published_data": r.published_date,
            "Author": r.author,
            "domain": r.url.split("/")[2] if "://" in r.url else r.url
      }])

      df = pd.concat([df, new_row], ignore_index=True)
      
filtered_df = df.groupby('domain').size().reset_index(name="Count")
print(type(filtered_df))
      
# print(len(df))
# print(response)
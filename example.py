from exa_py import Exa


exa = Exa('----')

# query = input('Search here: ')

response = exa.search(
  query="coffee",
  num_results=5,
  type='keyword',
  include_domains=['https://www.tiktok.com'],
)

# for result in response.results:
#   print(f'Title: {result.title}')
#   print(f'URL: {result.url}')
#   print()

print(response)

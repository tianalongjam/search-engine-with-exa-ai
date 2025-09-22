from exa_py import Exa


exa = Exa('a2e035a2-d6dd-4860-9202-8df13b04f2b6')

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
import requests
from bs4 import BeautifulSoup
import re

url_base = "https://en.openrussian.org/ru/"

def get_context_for_word(word):

	try: 
		response = requests.get(url_base + word)
		
		# Check if the request was successful
		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'html.parser')
			content = soup.find('div', class_="section sentences")
			content = content.find('span', class_="ru")
			content = content.find_all('a')
			
			sentence = ""
			for link in content:
				sentence += link.get_text().replace(" ","")
				sentence += " "
				sentence = "".join(c for c in sentence if c.isalpha() or c == " ")
				
			return sentence
		else:
			print(f"Failed to retrieve the page. Status code: {response.status_code}")
	except:
		return ""

def main():
	get_context_for_word("привет")
	
if __name__ == '__main__':
	main()

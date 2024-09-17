import requests
from bs4 import BeautifulSoup
import re

url_base = "https://en.openrussian.org/ru/"

def get_context_for_word(word):
	response = requests.get(url_base + word)

	# Check if the request was successful
	if response.status_code == 200:
		soup = BeautifulSoup(response.text, 'html.parser')
	else:
		print(f"Failed to retrieve the page. Status code: {response.status_code}")

	content = soup.find('div', class_="section sentences")
	content = content.find('span', class_="ru")
	content = content.find_all('a')
	
	# TODO: Here is some problem with removing whitespaces after accented letters from the words. Otherwise it should be fine.
	sentence = ""
	for link in content:
		sentence += link.get_text().replace(" ","")
		sentence += " "
		
	return sentence
def main():
	get_context_for_word("привет")
	
if __name__ == '__main__':
	main()

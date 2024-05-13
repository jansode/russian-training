import settings

from file_handling import *
from word_functions import *
from session import *

def handle_commands(argv):
	if len(argv) > 1:
		settings.WORDLIST_FILE = settings.MOST_COMMON_WORDS
		
		if argv[1] == 'session':	
			if len(argv) > 2:
				wordlist_file = argv[2]
				if file_exists(wordlist_file):
					settings.WORDLIST_FILE = wordlist_file
			
			init_word_list_and_wordlist_file()
			save_words()

			session()
		else:
			if argv[1] == 'quiz':
				if len(argv[2]) > 2:
					wordlist_file = argv[2]
					if file_exists(wordlist_file):
						settings.WORDLIST_FILE = wordlist_file
				
				init_word_list_and_safefile()
				save_words()

				quiz_word(3)		
			elif argv[1] == 'guess':
				if len(argv[2]) > 2:
					wordlist_file = argv[2]
					if file_exists(wordlist_file):
						settings.WORDLIST_FILE = wordlist_file
				
				init_word_list_and_safefile()
				save_words()
				print(guess_word(argv[2]," ".join(argv[3:])))
			elif argv[1] == 'answer':
				if len(argv[2]) > 2:
					wordlist_file = argv[2]
					if file_exists(wordlist_file):
						settings.WORDLIST_FILE = wordlist_file
				
				init_word_list_and_safefile()
				save_words()
				translate(argv[2])
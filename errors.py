import sys

ERROR_WORDLIST_FORMATTING = "Wordlist formatting error: "

def display_error_and_exit(error_type, msg):
	print(error_type, end="")
	print(msg)
	sys.exit(1)
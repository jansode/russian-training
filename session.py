import settings
from word_functions import *
from file_handling import *

# returns a tuple of booleans. (right answer check after this function?,get new question after?)
def handle_commands(command_string):
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: handle_commands")
		
	if command_string == "":
		return (False,False)
	elif command_string == "exit":
		save_words()
		exit(0)
	elif command_string == "dictionary":
		list_words()
		return (False,True)
	elif command_string == "problem_words":
		list_problem_words()
		return (False,True)
	elif command_string == "help":
		print("exit: Exits the program.")
		print("dictionary: Shows a list of the words the program knows.")
		print("set: Modify program settings.")
		print("\tdebug_function (true/false): Turn function call debug info on or off.")
		print("wordfile [wordfile_name]: Change word file.")
		print("problem_words: List words that have a low score.")
		print("help: Shows this text")
		print("")
		return (False,True)
		
	splitted = command_string.split(" ")
	if splitted[0] == "set":
		if len(splitted) != 3:
			print(settings.INVALID_COMMAND_TEXT)
			return (False,False)
		
		if splitted[1] == "debug_function":
			if splitted[2] == "true":
				settings.DEBUG_FUNCTION_CALL = True
				print("Function call debug info turned on.")

			elif splitted[2] == "false":
				settings.DEBUG_FUNCTION_CALL = False
				print("Function call debug info turned off.")
			else:
				print(settings.INVALID_COMMAND_TEXT)
		else:
			print(settings.INVALID_COMMAND_TEXT)

		return (False,False)
	elif splitted[0] == "wordfile":
		if len(splitted) != 2:
			print(settings.INVALID_COMMAND_TEXT)
			return (False,False)
		
		if file_exists(splitted[1]):
			save_words()
		
			global wordlist
			wordlist = []
			
			settings.WORDLIST_FILE = splitted[1]
			
			init_word_list_and_wordlist_file()
			save_words()
			
			return (False,False)
		else:
			print(settings.INVALID_COMMAND_TEXT)
			print("The specified word file does not exist.")
			return (False,False)
	else:
		return (True,True)

def session():
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: session")
	
	got_answer_from_previous = False
	did_command_in_previous = False
	(to_guess, correct_index) = quiz_word(settings.NUMBER_OF_SUGGESTIONS)
	
	while(True):
	
		if got_answer_from_previous or did_command_in_previous:
			(to_guess, correct_index) = quiz_word(settings.NUMBER_OF_SUGGESTIONS)
			
		print(">>",end='')
		guess = input() # Both number in list and word input works.
		word = get_word_object(to_guess)

		(continue_further, did_command_in_previous) = handle_commands(guess.strip())
		if not continue_further:
			got_answer_from_previous = False
			continue
		
		guess_word_correct = guess_word(wordlist,to_guess,guess)
		if not guess_word_correct and not guess.isnumeric():
			print(settings.INVALID_COMMAND_TEXT)
			continue

		if guess_word_correct or (int(guess) == correct_index):
			word.times_correct += 1
		
			success_rate = str(round(float(word.times_correct / word.times_encountered),2))
			if word.times_encountered == 0:
				success_rate = 0
				
			print("Correct! Progress with this word (success rate): "+success_rate)
			if settings.SHOW_TIMES_ENCOUNTERED:
				print("Times encountered: "+str(word.times_encountered))
			if settings.SHOW_TIMES_CORRECT:
				print("Times correct: "+str(word.times_correct))
			print("\n")
			
			update_wordlist_data(word)
		else:
			success_rate = str(float(word.times_correct / word.times_encountered))
			if word.times_encountered == 0:
				success_rate = 0
				
			print("Wrong! Progress with this word (success rate): "+success_rate + "\n")
			print("Correct translations: ")
			translate(word.in_russian)
		
		got_answer_from_previous = True
		save_words()
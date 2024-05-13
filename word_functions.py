import settings
import random
from numpy.random import choice

wordlist = []
english_word_set = set()

class Word:
	def __init__(self, russian, translations, function, times_encountered = 0, times_correct = 0):
		self.in_russian = russian
		self.translations = translations
		self.function = function
		self.times_encountered = times_encountered
		self.times_correct = times_correct

	def __str__(self):
		return self.in_russian + " ("+str(self.translations)+")\n\tfunction: " \
		+self.function+"\n\ttimes encountered: "+str(self.times_encountered)+"\n\ttimes correct: "+str(self.times_correct)+""
		
	def get_correct_rate(self):
		if self.times_encountered == 0:
			return 0

		return self.times_correct / self.times_encountered
		
def custom_split(string,delimeter,ignore_inside_char):
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: custom_split")
	output_list = []
	inside_safe_zone = False
	word = ""
	for char in string:
		if char == ignore_inside_char:
			inside_safe_zone = not inside_safe_zone
			continue

		if not inside_safe_zone and char == delimeter:
			output_list.append(word)
			word = ""
		else:
			word += char
	if len(word) > 0:
		output_list.append(word)
	return output_list
	
# Used in weighted choices function when choosing word to guess.
def get_wordlist_correct_rates():
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: get_wordlist_correct_rates")
	return_list = []
	for word in wordlist:
		correct_rate = word.get_correct_rate()
		if correct_rate == 0:
			correct_rate = 0.1
			
		return_list.append(correct_rate)

	# Normalize weights so that they sum up to 1.
	total = sum(return_list)
	normalized_weights = [weight / total for weight in return_list]

	return normalized_weights
	
def quiz_word(nr_suggestions):
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: quiz_word")

    # Choose words that have lower correct rate with higher probability.
	correct_rates_list = get_wordlist_correct_rates()
	translate_this = choice(wordlist, len(correct_rates_list), p=correct_rates_list)[0]

	copy_set = english_word_set.copy()
	for word in translate_this.translations:
		copy_set.remove(word.strip())

	false_words = random.sample(list(copy_set),nr_suggestions-1)
	
	# It would be cool to see an infinite loop here. 
	i = 0
	while True:
		if translate_this.translations[i].lstrip() not in false_words:
			false_words.append(translate_this.translations[i].lstrip())
			break
		i+=1
	
	random.shuffle(false_words)
	print("translate:"+translate_this.in_russian)
	print("suggestions:", end='')
	
	index = 1
	for word in false_words[:-1]:
		print(" ("+str(index)+") "+word.lstrip(), end=' |')
		index+=1

	print(" ("+str(index)+") "+false_words[-1].lstrip())

    # Get index of correct answer.
	correct_index = 0
	for i in range(len(false_words)):
		for translation in translate_this.translations:
			if false_words[i] == translation.lstrip():
				correct_index = (i+1)
				break

	return (translate_this.in_russian, correct_index)

def guess_word(wordlist,russian,english):
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: guess_word")

	for word_object in wordlist:
		if word_object.in_russian == russian:
			word_object.times_encountered += 1 
			for english_word in word_object.translations:
				if english in english_word.strip():
					word_object.times_correct += 1
					return True
	return False

def get_word_object(russian):
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: get_word_object")
	for word_object in wordlist:
		if word_object.in_russian == russian:
			return word_object

def translate(russian):
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: translate")
	for word_object in wordlist:
		if word_object.in_russian == russian:
			print(word_object.translations)

def update_wordlist_data(word):
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: update_wordlist_data")

	for i in range(len(wordlist)):
		if wordlist[i].in_russian == word.in_russian:
			wordlist[i] = word
			return

def list_words():
	for word in wordlist:
		print(word)
		
def list_problem_words():
	for word in wordlist:
		correct_rate = word.get_correct_rate()
		if (correct_rate < settings.PROBLEM_WORD_THRESHOLD) and (correct_rate != 0):
			print(word)

def word_frequency_from_text(argv[2]):
	pass



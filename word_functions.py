import settings
import random
import re
import string
import word_context_scraper
from termcolor import colored

from translate import Translator
from numpy.random import choice

import file_handling

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

	choice_index = random.randint(0,6)
	candidates = sorted(wordlist, key=lambda x:x.get_correct_rate())[:choice_index+1]
	translate_this = choice(candidates)

	copy_set = english_word_set.copy()
	for word in translate_this.translations:
		copy_set.remove(word.strip())

	false_words = random.sample(list(copy_set),nr_suggestions-1)
	
	i = 0
	while True:
		if translate_this.translations[i].lstrip() not in false_words:
			false_words.append(translate_this.translations[i].lstrip())
			break
		i+=1
	
	random.shuffle(false_words)
	
	context = ""
	if settings.DOWNLOAD_WORD_CONTEXT:
		context = word_context_scraper.get_context_for_word(translate_this.in_russian)
	
	print(colored("translate:",settings.MISC_COLOR)+colored(translate_this.in_russian,settings.QUIZ_WORD_COLOR))
	if context != "":
		print(colored("context: ",settings.MISC_COLOR)+colored(context,settings.QUIZ_WORD_COLOR))
	print(colored("suggestions:",settings.MISC_COLOR), end='')
	
	index = 1
	for word in false_words[:-1]:
		print(colored(" ("+str(index)+") ",settings.MISC_COLOR2)+colored(word.lstrip(),settings.QUIZ_WORD_COLOR), end=colored(' |',settings.MISC_COLOR2))
		index+=1

	print(colored(" ("+str(index)+") ",settings.MISC_COLOR2)+colored(false_words[-1].lstrip(),settings.QUIZ_WORD_COLOR))

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
			return word_object.translations

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

def word_frequency_from_text(filename,reverse=False,output_file=False,output_file_name="default.csv"):
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: word_frequency_from_text")
		
	word_occurences = {}
	
	if file_handling.file_exists(filename):
		text = file_handling.get_file_text_as_string(filename)
		
		for word in text.split(' '):
			plain_word = word.lower().replace('\n','').replace('\t','').replace('\r','')
			
			translator = plain_word.maketrans('','',string.punctuation)
			plain_word=plain_word.translate(translator)
			if len(plain_word) < 5:
				continue
			
			if plain_word not in word_occurences.keys():
				word_occurences[plain_word] = 1
			else:
				word_occurences[plain_word] = word_occurences[plain_word] + 1
		
		word_occurences = dict(sorted(word_occurences.items(), key=lambda item: item[1],reverse=reverse))
		print(len(word_occurences))

		start_print = 0
		nr_print = 100
		index = 0
		for word in word_occurences:
			if index > start_print:
				print(word,end=' ')
				print(word_occurences[word])
			index+=1
			
			if index == start_print+nr_print:
				break	
				
		if output_file:
			while file_handling.file_exists(output_file_name):
				split_name = output_file_name.split('.')
				split_name[0] += '_'
				output_file_name = split_name[0] +'.'+ split_name[1]
				
		'''
		with open(output_file, 'wb') as f:
			start_print = 0
			nr_print = 100
			index = 0
			for word in word_occurences:
				if index > start_print:
					print(word)
					to_write = word +",\""+translator.translate(word)+"\"" #TODO
					f.write(to_write.encode('utf8'))
				index+=1
				
				if index == start_print+nr_print:
					break
		'''		
	else:
		print("Error: File does not exist.")



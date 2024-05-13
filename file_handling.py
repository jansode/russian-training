import os
import settings
import codecs
from pathlib import Path
from word_functions import *

def save_file_exists():
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: save_file_exists")
	return Path(os.path.dirname(os.path.realpath(__file__)) + '\\' + "savefile_"+settings.WORDLIST_FILE.split('.')[0]+".txt").is_file()
	
def file_exists(file):
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: word_file_exists")
	return Path(os.path.dirname(os.path.realpath(__file__)) + '\\' + file).is_file()

def save_words():
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: save_words")
	with open('savefile_'+settings.WORDLIST_FILE.split(".")[0]+'.txt', 'wb') as f:
		for word in wordlist:
			to_write = word.in_russian + "|" + ",".join(word.translations) + "|" + word.function + "|" + str(word.times_encountered) + '|' + str(word.times_correct) +"\n"
			f.write(to_write.encode('utf8'))
		f.close()
		
def load_save_file():
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: load_save_file")
	with codecs.open('savefile_'+settings.WORDLIST_FILE.split(".")[0]+'.txt','r','utf-8') as f:
		lines = f.readlines()

		for line in lines:
			split_line = line.split('|')
			if len(split_line) > 1:
				english_words = split_line[1].split(",")
				for word in english_words:
					english_word_set.add(word.strip())
				wordlist.append(Word(split_line[0],english_words,split_line[2],int(split_line[3]), int(split_line[4])))

def create_save_file():
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: create_save_file")
	with codecs.open(settings.WORDLIST_FILE,'r','utf-8') as f:
		lines = f.readlines()

		for line in lines:
			split_line = custom_split(line,',','"')
			
			if len(split_line) > 1:	
				english_words = split_line[1].split(",")
				for word in english_words:
					english_word_set.add(word.strip())
					
				for i in range(len(english_words)):
					english_words[i] = english_words[i].strip().replace('\n','')
				
				word_function = ""
				if len(split_line) == 3:
					word_function = split_line[2].replace('\n','')
					
				wordlist.append(Word(split_line[0],english_words,word_function))
	
	save_words()
	
def init_word_list_and_wordlist_file():
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: init_word_list_and_wordlist_file")
	if save_file_exists():
		load_save_file()
		sync_save_file_with_new_words()
	else:
		create_save_file()


def sync_save_file_with_new_words():
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: sync_save_file_with_new_words")
			
	words = []
	with codecs.open(settings.WORDLIST_FILE,'r','utf-8') as f:
		lines = f.readlines()

		for line in lines:
			split_line = custom_split(line,',','"')
			if len(split_line) > 1:
				english_words = split_line[1].replace('\n','').split(",")
				
				word_function = ""
				if len(split_line) == 3:
					word_function = split_line[2].replace('\n','')
				
				words.append(Word(split_line[0],english_words,word_function))
	
	words_added = 0
	for word in words:
		if not any(x.in_russian == word.in_russian for x in wordlist):
			words_added += 1		
			for w in word.translations:
				english_word_set.add(w.strip())		
			
			wordlist.append(word)
	
	if words_added > 0:
		print("Wordfile and wordlist_file synced. "+str(words_added)+" new words added.")

def get_file_text_as_string(filename):
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: get_file_text_as_string")
	
	output_text = ""
	with codecs.open(filename,'r','utf-8') as f:
		lines = f.readlines()

		for line in lines:
			output_text += line
	
	return output_text
				
	
	
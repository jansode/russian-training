import os
import sys
import codecs
import random
from numpy.random import choice
from pathlib import Path

MOST_COMMON_WORDS = "most_common_words.csv"

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

wordlist = []
english_word_set = set()

class Word:
    def __init__(self, russian, translations, function, times_encountered = 0, times_correct = 0):
        self.in_russian = russian
        self.translations = translations
        self.function = function
        self.times_encountered = times_encountered
        self.times_correct = 0

    def get_correct_rate(self):
        if self.times_encountered == 0:
            return 0

        return self.times_correct / self.times_encountered

# Used in weighted choices function when choosing word to guess.
def get_wordlist_correct_rates():
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

def custom_split(string,delimeter,ignore_inside_char):
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

def save_file_exists(wordlist):
    return Path(os.path.dirname(os.path.realpath(__file__)) + '\\' + "savefile_"+wordlist.split(',')[0]+".txt").is_file()

def save_words(word_list_file):
    with open('savefile_'+word_list_file.split(".")[0]+'.txt', 'wb') as f:
        for word in wordlist:
            to_write = word.in_russian + "|" + ",".join(word.translations) + "|" + word.function + "|" + str(word.times_encountered) + '|' + str(word.times_correct) +"\n"
            f.write(to_write.encode('utf8'))
        f.close()

def load_save_file(word_list):
    with codecs.open('savefile_'+word_list+'.txt','r','utf-8') as f:
        lines = f.readlines()

        for line in lines:
            split_line = line.split('|')
            english_words = split_line[1].split(",")
            for word in english_words:
                english_word_set.add(word.strip())
            wordlist.append(Word(split_line[0],english_words,split_line[2],int(split_line[3]), int(split_line[4])))

def create_save_file(word_list):
	with codecs.open(word_list,'r','utf-8') as f:
		lines = f.readlines()

		for line in lines:
			split_line = custom_split(line,',','"')
			english_words = split_line[1].split(",")
			for word in english_words:
				english_word_set.add(word.strip())
				
			for i in range(len(english_words)):
				english_words[i] = english_words[i].strip()

			wordlist.append(Word(split_line[0],english_words,split_line[2].replace('\n','')))
	
	save_words(word_list)
	
def quiz_word(word_list, suggestions):

	print("quiz_word -> suggestions: "+str(suggestions))
	
	
	
    # Choose words that have lower correct rate with higher probability.
	correct_rates_list = get_wordlist_correct_rates()
	translate_this = choice(wordlist, len(correct_rates_list), p=correct_rates_list)[0]

	copy_set = english_word_set.copy()
	for word in translate_this.translations:
		copy_set.remove(word.strip())

	'''
	false_word_set = english_word_set.copy()
	
	for word in translate_this.translations:
		false_word_set = false_word_set - set(word)
	'''
	false_words = random.sample(list(copy_set),suggestions-1)
	print("False words:" +str(false_words))
	
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
	
	for word in false_words[:-1]:
		print(word.lstrip(), end='|')

	print(false_words[-1].lstrip(), end='')

    # Get index of correct answer.
	# For now we can have multiple correct indices. TODO maybe.
	# I just don't want to think about this now. It should be just one.
	correct_index = 0
	for i in range(len(false_words)):
		for translation in translate_this.translations:
			if false_words[i] == translation.lstrip():
				correct_index = (i+1)
				break

	return (translate_this.in_russian, correct_index)

def guess_word(wordlist,russian,english):
    for word_object in wordlist:
        if word_object.in_russian == russian:
            word_object.times_encountered += 1 
            for english_word in word_object.translations:
                if english in english_word.strip():
                    word_object.times_correct += 1
                    return True
    return False

def get_word_object(russian):
    for word_object in wordlist:
        if word_object.in_russian == russian:
            return word_object

def translate(wordlist,russian):
    for word_object in wordlist:
        if word_object.in_russian == russian:
            print(word_object.translations)

def session(word_list):
	while(True):
		(to_guess, correct_index) = quiz_word(word_list,3)
		print("\n>>",end='')
		guess = input() # Both number in list and word input works.
		word = get_word_object(to_guess)

		if guess_word(wordlist,to_guess,guess) or (int(guess) == correct_index):
			success_rate = str(float(word.times_correct / word.times_encountered))
			if word.times_encountered == 0:
				success_rate = 0
				
			print("Correct! Progress with this word (success rate): "+success_rate + "\n")
		else:
			success_rate = str(float(word.times_correct / word.times_encountered))
			if word.times_encountered == 0:
				success_rate = 0
				
			print("Wrong! Progress with this word (success rate): "+success_rate + "\n")
			print("Correct translations: ")
			translate(wordlist,word.in_russian)

def init_word_list_and_savefile(wordlist):
	if save_file_exists(wordlist):
		load_save_file(wordlist)
	else:
		create_save_file(wordlist)

def main():
	if len(sys.argv) > 1:
		wordlist = MOST_COMMON_WORDS
		
		if sys.argv[1] == 'session':	
			if len(sys.argv) > 2:
				wordlist = sys.argv[2]
			
			init_word_list_and_savefile(wordlist)
			save_words(wordlist)

			session(wordlist)

		else:
			if sys.argv[1] == 'quiz':
				if len(sys.argv[2]) > 2:
					wordlist = sys.argv[2]
				
				init_word_list_and_safefile(wordlist)
				save_words(wordlist)

				quiz_word(wordlist,3)		
			elif sys.argv[1] == 'guess':
				if len(sys.argv[2]) > 2:
					wordlist = sys.argv[2]
				
				init_word_list_and_safefile(wordlist)
				save_words(wordlist)
				print(guess_word(wordlist,sys.argv[2]," ".join(sys.argv[3:])))
			elif sys.argv[1] == 'answer':
				if len(sys.argv[2]) > 2:
					wordlist = sys.argv[2]
				
				init_word_list_and_safefile(wordlist)
				save_words(wordlist)
				translate(wordlist,sys.argv[2])

		#save_words(wordlist)

if __name__ == '__main__':
    main()

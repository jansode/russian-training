import os
import sys
import codecs
import random
from numpy.random import choice
from pathlib import Path

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

# Used in weighte choices function when choosing word to guess.
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

def save_file_exists():
    return Path(os.path.dirname(os.path.realpath(__file__)) + '\\' + "savefile.txt").is_file()

def save_words():
    with open('savefile.txt', 'wb') as f:
        for word in wordlist:
            to_write = word.in_russian + "|" + ",".join(word.translations) + "|" + word.function + "|" + str(word.times_encountered) + '|' + str(word.times_correct) +"\n"
            f.write(to_write.encode('utf8'))
        f.close()

def load_save_file():
    with codecs.open('savefile.txt','r','utf-8') as f:
        lines = f.readlines()

        for line in lines:
            split_line = line.split('|')
            english_words = split_line[1].split(",")
            for word in english_words:
                english_word_set.add(word)
            wordlist.append(Word(split_line[0],english_words,split_line[2],int(split_line[3]), int(split_line[4])))

def create_save_file():
    with codecs.open('words.csv','r','utf-8') as f:
        lines = f.readlines()

        for line in lines:
            split_line = custom_split(line,',','"')
            english_words = split_line[1].split(",")
            for word in english_words:
                english_word_set.add(word)
            wordlist.append(Word(split_line[0],english_words,split_line[2].replace('\n','')))

def quiz_word(suggestions):

    # Choose words that have lower correct rate with higher probability.
    correct_rates_list = get_wordlist_correct_rates()
    translate_this = choice(wordlist, len(correct_rates_list), p=correct_rates_list)[0]

    false_words = random.sample(english_word_set,suggestions-1)
    false_words.append(translate_this.translations[0].lstrip())
    random.shuffle(false_words)
    print("translate:"+translate_this.in_russian)
    print("suggestions:", end='')

    for word in false_words[:-1]:
        print(word.lstrip(), end='|')

    print(false_words[-1].lstrip(), end='')

    # Get index of correct answer.
    correct_index = 0
    for i in range(len(false_words)):
        if false_words[i] == translate_this.translations[0].lstrip():
            correct_index = i
            break

    return (translate_this.in_russian, correct_index+1)

def guess_word(russian,english):
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

def translate(russian):
    for word_object in wordlist:
        if word_object.in_russian == russian:
            print(word_object.translations)

def session():
    while(True):
        (to_guess, correct_index) = quiz_word(3)
        print("\n>>",end='')
        guess = input() # Both number in list and word input works.
        word = get_word_object(to_guess)


        if guess_word(to_guess,guess) or int(guess) == correct_index:
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
            translate(word.in_russian)

def main():
    if save_file_exists():
        load_save_file()
    else:
        create_save_file()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'session':
            session()

        else:
            if sys.argv[1] == 'quiz':
                quiz_word(3)
            elif sys.argv[1] == 'guess':
                print(guess_word(sys.argv[2]," ".join(sys.argv[3:])))
            elif sys.argv[1] == 'answer':
                translate(sys.argv[2])

    save_words()

if __name__ == '__main__':
    main()

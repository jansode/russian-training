import settings
from word_functions import *
from file_handling import *
from termcolor import colored
from playsound import playsound
from moviepy.editor import VideoFileClip
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
import pygame
import threading
import queue
import os
import platform
import webbrowser

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
	elif command_string == "clear":
		
		my_os = platform.system()
		if my_os == 'Linux':
			os.system("clear")
		elif my_os == 'Windows':
			os.system("cls")
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

music_list = ["bg_lp_most.mp3","bg_lp_middle.mp3","bg_lp_better.mp3","bg_lp_best.mp3","bg_level1.mp3","bg_level2.mp3","bg_level3.mp3","bg_level4.mp3","bg_level5.mp3","bg_level6.mp3","bg_level7.mp3"]
curr_level = 0
curr_points = 0
curr_combo = 0
next_level_threshold = settings.POINTS_TO_LEVEL_UP

def level_screen(screen):
	effects = [
		Cycle(
			screen,
			FigletText("LEVEL 12!", font='big'),
			int(screen.height / 2 - 8)),
		Cycle(
			screen,
			FigletText("Press any key...", font='small'),
			int(screen.height / 2 + 3)),
			Stars(screen, 200)
		]
	screen.play([Scene(effects, 500)],repeat=False)

	
def change_level(up_or_down):
	global curr_level
	
	changed = False
	if up_or_down == "UP":
		curr_level = (curr_level + 1)
		changed = True
		playsound('level_up_sound.mp3')
		print(colored("LEVEL UP!!!",settings.CORRECT_COLOR))
	elif up_or_down == "DOWN":
		curr_level = (curr_level - 1)
		changed = True
		playsound('level_down_sound.mp3')

		if curr_level < 0:
			curr_level = 0
	else:
		print("Why do you even try to use this program?")

	if changed:
		curr_pos = pygame.mixer.music.get_pos()
		
		what_do = settings.DO_AT_LEVELUP[curr_level]
		
		if what_do == settings.NEXT_MUSIC:
			pygame.mixer.music.stop()
			pygame.mixer.music.load(music_list[curr_level])
			pygame.mixer.music.play(loops=-1,start=(curr_pos/1000))
		elif what_do == settings.VIDEO_PRIZE1:
			url = "https://www.youtube.com/watch?v=m6pE8psWJXE"
			webbrowser.open(url, new=0, autoraise=True)
		elif what_do == settings.ASCII_PRIZE1:
			Screen.wrapper(level_screen)
			
		
			
def session():
	if settings.DEBUG_FUNCTION_CALL:
		print("CALL: session")
	
	global music_list, curr_level, curr_points, curr_combo, next_level_threshold
	
	pygame.init()

	pygame.mixer.music.load(music_list[curr_level])
	pygame.mixer.music.play(loops=-1)
	
	got_answer_from_previous = False
	did_command_in_previous = False
	(to_guess, correct_index) = quiz_word(settings.NUMBER_OF_SUGGESTIONS)

	while(True):
	
		if got_answer_from_previous or did_command_in_previous:
			(to_guess, correct_index) = quiz_word(settings.NUMBER_OF_SUGGESTIONS)
			
		print(colored(">>",settings.MISC_COLOR),end='')
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
				
			print(colored("Correct! Progress with this word (success rate): "+success_rate,settings.CORRECT_COLOR))
			if settings.SHOW_TIMES_ENCOUNTERED:
				print(colored("Times encountered: "+str(word.times_encountered),settings.CORRECT_COLOR))
			if settings.SHOW_TIMES_CORRECT:
				print(colored("Times correct: "+str(word.times_correct),settings.CORRECT_COLOR))

			playsound('correct_sound.mp3')
			update_wordlist_data(word)
			
			added_points = settings.POINTS_FOR_CORRECT
			if curr_combo == 3:
				added_points = settings.POINTS_FOR_COMBO_3
			elif curr_combo == 5:
				added_points = settings.POINTS_FOR_COMBO_5
			elif curr_combo == 10:
				added_points = settings.POINTS_FOR_COMBO_10
			
			curr_points = curr_points + added_points
			if curr_points >= next_level_threshold:
				change_level("UP")
				next_level_threshold = next_level_threshold + settings.POINTS_TO_LEVEL_UP
			
			print(colored("Points: "+str(curr_points),settings.CORRECT_COLOR)+ " "+ colored("(+"+str(added_points)+") Level: "+str(curr_level),settings.CORRECT_COLOR))
			

		else:
			success_rate = str(round(float(word.times_correct / word.times_encountered),2))
			if word.times_encountered == 0:
				success_rate = 0
				
			curr_points = curr_points - settings.POINTS_RETRACTED_FOR_WRONG
			if curr_points < 0:
				curr_points = 0
				
			print(colored("Wrong! Progress with this word (success rate): "+success_rate+"",settings.WRONG_COLOR))
			print(colored("Correct translations: ",settings.WRONG_COLOR))
			print(colored(translate(word.in_russian),settings.WRONG_COLOR))
			print(colored("Points: "+str(curr_points),settings.WRONG_COLOR)+" "+colored("(-"+str(settings.POINTS_RETRACTED_FOR_WRONG)+") Level: "+str(curr_level),settings.WRONG_COLOR))
			playsound('wrong_sound.mp3')
			
			#change_level("DOWN")

		
		got_answer_from_previous = True
		save_words()
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
import errors
import time
import random
import tetris

music_list = settings.MUSIC_LIST
curr_level = 0
curr_points = 0
curr_combo = 0
next_level_threshold = settings.POINTS_TO_LEVEL_UP

def print_help():
	print("exit: Exits the program.")
	print("dictionary: Shows a list of the words the program knows.")
	print("set: Modify program settings.")
	print("\tdebug_function (true/false): Turn function call debug info on or off.")
	print("wordfile [wordfile_name]: Change word file.")
	print("problem_words: List words that have a low score.")
	print("clear: Clears the screen.")
	print("music (on/off): Toggle music")
	print("effects (on/off): Toggle sound effects")
	print("tetris: Starts a game of tetris.")
	print("flag: Draws the russian flag.")
	print("help: Shows this text")
	print("")

def set_music(on_or_off):
	if on_or_off == "ON":
		settings.MUSIC_ON = True
		
		global music_list, curr_level
		if curr_level < settings.MAX_MUSIC_LEVEL:
			pygame.mixer.music.load(music_list[curr_level])
		else:
			pygame.mixer.music.load(music_list[MAX_MUSIC_LEVEL])
			
		pygame.mixer.music.play(loops=-1)
	elif on_or_off == "OFF":
		settings.MUSIC_ON = False
		pygame.mixer.music.stop()

def draw_flag():
	print(colored("###################",settings.WHITE_COLOR))
	print(colored("###################",settings.WHITE_COLOR))
	print(colored("###################",settings.MISC_COLOR))
	print(colored("###################",settings.MISC_COLOR))
	print(colored("###################",settings.WRONG_COLOR))
	print(colored("###################",settings.WRONG_COLOR))

		
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
		
	elif command_string == "flag":
		draw_flag()
		return (False,False)
	elif command_string == "tetris":
		tetris.start_tetris()
		return (False,False)
	elif command_string == "clear":	
		my_os = platform.system()
		if my_os == 'Linux':
			os.system("clear")
		elif my_os == 'Windows':
			os.system("cls")
		return (False,True)
	elif command_string == "help":
		print_help()
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
	elif splitted[0] == "music":
	
		if splitted[1] == "on":
			set_music("ON")
		elif splitted[1] == "off":
			set_music("OFF")
			
		return (False,False)
	elif splitted[0] == "effects":
		if splitted[1] == "on":
			settings.EFFECTS_ON = True
		elif splitted[1] == "off":
			settings.EFFECTS_ON = False
			
		return (False,False)
	else:
		return (True,True)


def level_screen(screen):
	global curr_level

	effects = [
		Cycle(
			screen,
			FigletText("LEVEL "+str(curr_level)+" !", font='big'),
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
		if settings.EFFECTS_ON:
			playsound(settings.LEVEL_UP_SOUND)
		print(colored("LEVEL UP!!!",settings.CORRECT_COLOR))
		
	elif up_or_down == "DOWN":
		curr_level = (curr_level - 1)
		changed = True
		if settings.EFFECTS_ON:
			playsound('level_down_sound.mp3')

		if curr_level < 0:
			curr_level = 0
	else:
		print("Why do you even try to use this program?")

	if changed:
		curr_pos = pygame.mixer.music.get_pos()
		
		what_do = settings.DO_AT_LEVELUP[curr_level] if curr_level in settings.DO_AT_LEVELUP else settings.DO_LAST_INDEFINITELY
		Screen.wrapper(level_screen)
		
		if what_do == settings.NEXT_MUSIC:
			pygame.mixer.music.stop()
			pygame.mixer.music.load(music_list[curr_level])
			if settings.MUSIC_ON:
				pygame.mixer.music.play(loops=-1,start=(curr_pos/1000))
		elif what_do == settings.VIDEO_PRIZE1:
			url = settings.VIDEO_PRIZE1
			webbrowser.open(url, new=0, autoraise=True)
			
		'''
		elif what_do == settings.ASCII_PRIZE1 or settings.DO_LAST_INDEFINITELY:
			Screen.wrapper(level_screen)
		'''

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
			
			if settings.EFFECTS_ON:
				playsound(settings.CORRECT_SOUND)
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
			if settings.EFFECTS_ON:
				playsound(settings.WRONG_SOUND)
		
		got_answer_from_previous = True
		save_words()
DEBUG_FUNCTION_CALL = False

DOWNLOAD_WORD_CONTEXT = True

MUSIC_ON = True
EFFECTS_ON = True

SAVEFOLDER = "savefiles"
WORDLISTFOLDER = "wordlists"
MOST_COMMON_WORDS = "most_common_words.csv"
WORDLIST_FILE = "custom_words.csv"

SHOW_TIMES_ENCOUNTERED = True
SHOW_TIMES_CORRECT = True

INVALID_COMMAND_TEXT = "Invalid command..."

NUMBER_OF_SUGGESTIONS = 3
PROBLEM_WORD_THRESHOLD = 0.4

QUIZ_WORD_COLOR = "light_grey"
CORRECT_COLOR = "light_green"
WRONG_COLOR = "red"
MISC_COLOR = "light_blue"
MISC_COLOR2 = "light_red"
WHITE_COLOR = "white"

MAX_MUSIC_LEVEL = 10
POINTS_TO_LEVEL_UP = 400
POINTS_FOR_CORRECT = 100
POINTS_FOR_COMBO_3 = 300
POINTS_FOR_COMBO_5 = 500
POINTS_FOR_COMBO_10 = 1000
POINTS_RETRACTED_FOR_WRONG = 50

NEXT_MUSIC = "next music"
VIDEO_PRIZE1 = "https://www.youtube.com/watch?v=m6pE8psWJXE"
ASCII_PRIZE1 = "ascii1"
DO_LAST_INDEFINITELY = "last_indefinitely"

MUSIC_LIST = [
	"audio/bg_lp_most.mp3",
	"audio/bg_lp_middle.mp3",
	"audio/bg_lp_better.mp3",
	"audio/bg_lp_best.mp3",
	"audio/bg_level1.mp3",
	"audio/bg_level2.mp3",
	"audio/bg_level3.mp3",
	"audio/bg_level4.mp3",
	"audio/bg_level5.mp3",
	"audio/bg_level6.mp3",
	"audio/bg_level7.mp3"
]

WRONG_SOUND = 'audio/wrong_sound.mp3'
CORRECT_SOUND = 'audio/correct_sound.mp3'
LEVEL_UP_SOUND = 'audio/level_up_sound.mp3'

DO_AT_LEVELUP = {
	1 : NEXT_MUSIC,
	2 : NEXT_MUSIC,
	3 : NEXT_MUSIC,
	4 : NEXT_MUSIC,
	5 : NEXT_MUSIC,
	6 : NEXT_MUSIC,
	7 : NEXT_MUSIC,
	8 : NEXT_MUSIC,
	9 : NEXT_MUSIC,
	10 : NEXT_MUSIC,
	11 : VIDEO_PRIZE1,
	12 : ASCII_PRIZE1,
}



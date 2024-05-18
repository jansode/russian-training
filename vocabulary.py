import sys
import codecs
import platform

from commands import *

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

my_os = platform.system()

if my_os == 'Linux':
	os.system('setterm -background black -foreground grey -store')
	os.system("clear")
elif my_os == 'Windows':
	os.system('color 07')
	os.system("cls")
	
def main():
	handle_commands(sys.argv)

if __name__ == '__main__':
    main()

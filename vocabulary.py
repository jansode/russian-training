import sys
import codecs

from commands import *

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def main():
	handle_commands(sys.argv)

if __name__ == '__main__':
    main()

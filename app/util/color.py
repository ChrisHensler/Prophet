import math

color_prefix='\x1b['

#color defintions
red = color_prefix +'1;31m'
green = color_prefix +'1;32m'
yellow = color_prefix +'1;33m'
blue = color_prefix +'1;34m'
magenta = color_prefix +'1;35m'
cyan = color_prefix +'1;36m'
white = color_prefix +'1;37m'
neutral = color_prefix +'0m'


port_color=cyan
host_color=red
script_color=yellow
important_color=yellow
interesting_color=magenta
good_color = green
bad_color = red
info_color = blue

CONSOLE_COLOR = neutral

def setConsoleColor(color):
	CONSOLE_COLOR = color
	print(CONSOLE_COLOR)

def c_print(color, text):
	print(string(color,text))

def string(color, text):
	start = color
	end = CONSOLE_COLOR

	#join for supporting overlapping colors
	return start + start.join(list(text)) + end

if __name__=='__main__':
	c_print(red,"red!")
	c_print(green,"green!")
	c_print(yellow,"yellow!")
	c_print(blue,"blue!")
	c_print(magenta,"magenta!")
	c_print(cyan,"cyan!")
	c_print(white,"white!")
	c_print(neutral,"neutral!")

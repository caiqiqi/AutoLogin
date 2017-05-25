#coding=utf-8
import termcolor

def color(message, color):
	msg = termcolor.colored(str(message), str(color), attrs=["bold"])
	return msg


class Colors:
    white = "\033[1;37m"
    normal = "\033[0;00m"
    red = "\033[1;31m"
    blue = "\033[1;34m"
    green = "\033[1;32m"
    lightblue = "\033[0;34m"

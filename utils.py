import termcolor

def color(message, color):
	msg = termcolor.colored(str(message), str(color), attrs=["bold"])
	return msg
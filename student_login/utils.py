#coding=utf-8
import termcolor

def color(message, color):
	msg = termcolor.colored(str(message), str(color), attrs=["bold"])
	return msg


def banner(version):
    banner = """\n
            ___         __        __                _
           /   | __  __/ /_____  / /   ____  ____ _(_)___
          / /| |/ / / / __/ __ \/ /   / __ \/ __ `/ / __ \\
         / ___ / /_/ / /_/ /_/ / /___/ /_/ / /_/ / / / / /
        /_/  |_\__,_/\__/\____/_____/\____/\__, /_/_/ /_/
                                          /____/
[ AutoLogin - Login Automatically v{} ]\n
""".format(version)
    return color(banner,"blue")


class Colors:
    white = "\033[1;37m"
    normal = "\033[0;00m"
    red = "\033[1;31m"
    blue = "\033[1;34m"
    green = "\033[1;32m"
    lightblue = "\033[0;34m"

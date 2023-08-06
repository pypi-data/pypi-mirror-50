__CONSOLE_IMPORTED = False
try:
	import console
	console.set_font('Consolas', 10)
	__CONSOLE_IMPORTED = True
except:
	pass
import colorama
import sys
from multiprocessing import Lock

END = '\n'
mu = Lock()
colorama.init()

class __ender(object):
	def end(self):
		sys.stdout.write(END)
	
def set_color(r, g, b, clr):
	if __CONSOLE_IMPORTED:
		console.set_color(r, g, b)
	else:
		sys.stdout.write(clr)
	
def info(text):
	#mu.acquire()
	set_color(0.9, 1, 1, colorama.Fore.LIGHTCYAN_EX)
	unsafe_print('[INFO] ')
	unsafe_print(text)
	#mu.release()
	return __ender()
	
def err(text):
	#mu.acquire()
	set_color(1, 0.2, 0.1, colorama.Fore.RED)
	unsafe_print('[ERROR] ')
	unsafe_print(text)
	#mu.release()
	return __ender()
	
def warn(text):
	#mu.acquire()
	set_color(1, 1, 0, colorama.Fore.YELLOW)
	unsafe_print('[WARN] ')
	unsafe_print(text)
	#mu.release()
	return __ender()
	
def debug(text):
	#mu.acquire()
	set_color(0.8, 0.8, 0.8, colorama.Fore.WHITE)
	unsafe_print('[DEBUG] ')
	unsafe_print(text)
	#mu.release()
	return __ender()

def unsafe_print(text):
	return sys.stdout.write(text)
	
if __name__ == '__main__':
	
	info('Hello World').end()
	err('Hello World').end()
	warn('Hello World').end()
	debug('Hello World').end()

import ui
import threading
def background(func):
	t = threading.Thread(target=func)
	t.start()
	return t
def foreground(func):
	ui.in_background(func)()

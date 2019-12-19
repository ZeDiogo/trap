import os, sys
from pynput import mouse 
from pynput import keyboard
import ctypes

class patrol:

	def __init__(self):
		self.active = True

	def on_move(self, x, y):
		self.catchThief()
		return False

	def on_click(self, x, y, button, pressed):
		self.catchThief()
		return False

	def on_scroll(self, x, y, dx, dy):
		self.catchThief()
		return False

	def on_press(self, key):
		self.catchThief()
		return False

	def on_release(self, key):
		self.catchThief()
		return False

	def catchThief(self):
		self.active = False
		ctypes.windll.user32.LockWorkStation()
		return False

	def start(self):
		# ...or, in a non-blocking fashion:
		mlistener = mouse.Listener(
			on_move=self.on_move,
			on_click=self.on_click,
			on_scroll=self.on_scroll)
		mlistener.start()

		# ...or, in a non-blocking fashion:
		klistener = keyboard.Listener(
			on_press=self.on_press,
			on_release=self.on_release)
		klistener.start()
		while self.active:
			# wait
			pass
			

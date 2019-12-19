from slacker import Slacker
import json
import sys
import os

class slack:

	def __init__(self, me, ask_confirmation=False, as_user=False):
		self.workspace = Slacker(self.getToken())
		me = self.getUser(self.workspace.users.list(), me)
		self.username = me['profile']['display_name']
		self.image = me['profile']['image_512']
		self.config = os.path.abspath('config.json')
		self.as_user = as_user
		self.ask_confirmation = ask_confirmation

	def checkToken(self, token):
		workspace = Slacker(token)
		try:
			workspace.channels.list()
		except:
			# sys.exit("Token not valid: check {}".format(self.config)) # TODO: why is self.config not allowed here?
			sys.exit("Token not valid: check config file") # TODO: if no internet connection, returns this exception #FIX

	def getToken(self):
		try:
			config = 'config.json'
			with open(config) as f:
				vars = json.load(f)
				self.checkToken(vars['token'])
				return vars['token']
		except FileNotFoundError as fnfe:
			print('Token API not found')
			token = input('Please provide a valid token: ')
			self.checkToken(token)
			print('Creating file...')
			with open(config, 'w') as f:
				content = { "token" : token }
				json.dump(content, f)
			return token

	def upload(self):
		# Upload a file
		self.workspace.files.upload(file_='intruder.jpg', channels=['testing'])

	def getUser(self, response, destination):
		for user in response.body['members']:
			if not user['deleted']:
				if destination.lower() in user['profile']['real_name_normalized'].lower() or destination.lower() in user['profile']['display_name_normalized'].lower():
					return user
		return None

	def getChannel(self, response, destination):
		# for k, v in zip(response.body.keys(), response.body.values()):
		# 	print('{} : {}'.format(k,v))
		for channel in response.body['channels']:
			if destination.lower() in channel['name_normalized'].lower():
				return channel
		return None

	def send(self, msg, destination):
		channelsResponse = self.workspace.channels.list()
		userResponse = self.workspace.users.list()
		user = self.getUser(userResponse, destination)
		channel = self.getChannel(channelsResponse, destination)	# TODO: rearrange if's, so that dont need to be always executed
		# print(self.username)
		if user and self.confirm(user['profile']['real_name_normalized']):
			res = self.workspace.chat.post_message(user['id'], msg, username=self.username, icon_url=self.image, as_user=self.as_user)
			# print(res)
		elif channel and self.confirm(channel['name_normalized']):
			res = self.workspace.chat.post_message(channel['id'], msg, username=self.username, icon_url=self.image, as_user=self.as_user)
			# print(res)
		else:
			print('Message not sent')

	def confirm(self, destination):
		if self.ask_confirmation:
			response = input('The message will be sent to {}. Ok? ([Y]es/[N]o): '.format(destination))
			if response.lower() == 'y':
				return True
			else:
				return False
		return True

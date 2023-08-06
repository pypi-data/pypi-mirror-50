from xgram.telegram import *
import threading
import time
import json
import xgram.log as log

class Updater (object):
	
	def __init__(self, tlg, message = None, callback = None):
		self.__tlg__ = tlg
		self.__on_message__ = Updater.on_message
		self.__on_callback__ = Updater.on_callback
		self.update_id = 0
		
		if message is not None:
			self.__on_message__ = message
		
		if callback is not None:
			self.__on_callback__ = callback
		
	def __tick_updates(self):
		updates = self.__tlg__.get_updates(offset=self.update_id)
		
		if len(updates) == 0:
			return 0
			
		threads = []
		log.debug('New updates: {}'.format(len(updates))).end()
		
		for update in updates:
			try:
				threads.append(threading.Thread(target=self.update, args=(update,)))
				#self.update(update)
			except Exception as e:
				log.err(str(e)).end()
			if self.update_id <= update['update_id']:
				self.update_id = update['update_id']+1
		
		for th in threads:
			th.run()
		return len(updates)
		
	def update(self, update):
		for key in update:
			if key == 'message':
				self.__on_message__(self.__tlg__, update[key])
				continue
			if key == 'callback_query':
				self.__on_callback__(self.__tlg__, update[key])
				continue
			if key != 'update_id':
				log.warn('Undefined update ' + key).end()
				log.debug(json.dumps(update[key])).end()
				continue
		pass
	
	def run(self):
		me = self.__tlg__.get_me()
		log.info('Authorized of {} @{}'.format(me['first_name'], me['username'])).end()
		
		while True:
			if self.__tick_updates() == 0:
				time.sleep(2)
				pass
				
	def on_message(tlg, data):
		log.warn('A new message has arrived, but the corresponding handler is not assigned.').end()
		log.debug(json.dumps(data)).end()
		pass
	
	def on_callback(tlg, data):
		log.warn('A callback was detected, but no corresponding handler was assigned.').end()
		log.debug(json.dumps(data)).end()
		pass
	

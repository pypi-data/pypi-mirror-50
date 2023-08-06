import requests
import xgram.log as log
import time
import json

class TelegramException(Exception):
	def __init__(self, message, code):
		super().__init__(message)

def fix_none(n):
	to_remove = []
	
	for key in n:
			if n[key] is None:
				to_remove.append(key)
	for key in to_remove:
		del n[key]
		
	return n

def InlineKeyboard(data):
	return {'inline_keyboard': data}
	
def Keyboard(data):
	return {'keyboard': data}

def InlineKeyboardButton(text, url=None, login_url=None, callback_data=None, switch_inline_query=None, switch_inline_query_current_chat=None,
	callback_game=None, pay=False):
		btn = {
			'text': text, 
			'callback_data': callback_data,
			'url': url,
			'login_url': login_url,
			'switch_inline_query': switch_inline_query,
			'switch_inline_query_current_chat': switch_inline_query_current_chat,
			'callback_game':callback_game,
			'pay': pay
			}
		
		return fix_none(btn)
	
class Telegram(object):
	
	def __init__(self, token):
		self.__token__ = token
		
	def __api(self, method, options=None):
		if not options:
			options = {}
		
		request_url = 'https://api.telegram.org/bot{}/{}'.format(self.__token__, method)
		
		start = time.time()
		respone = requests.post(request_url, data=options).json()
		end = time.time()-start
		
		if end > 1:
			sz_in = len(json.dumps(options).encode('utf-8'))
			
			sz_out = len(json.dumps(respone).encode('utf-8'))
			
			log.warn('Long request detected.').end()
			log.debug('{} [{}s, data size: {}/{} bytes]'.format(request_url, end, sz_in, sz_out)).end()
		
		if respone['ok']:
			return respone['result']
		
		log.err('{}, code: {}'.format(respone['description'], respone['error_code'])).end()
		raise TelegramException(respone['description'], respone['error_code'])
		return None
		
	def get_me(self):
		return self.__api('getMe')
		
	def get_updates(self, offset=None):
		options = {}
		if offset is not None:
			options['offset'] = offset
		
		return self.__api('getUpdates', options=options)
	
	def edit_message_text(self, chat_id, message_id=None, inline_message_id=None, text=None, parse_mode=None, disable_web_page_preview=None, reply_markup=None):
		options = {
			'chat_id': chat_id,
			'message_id': message_id,
			'inline_message_id': inline_message_id,
			'text': text,
			'parse_mode': parse_mode,
			'disable_web_page_preview': 'disable_web_page_preview',
			'reply_markup': reply_markup
		}
		
		options = fix_none(options)
		return self.__api('editMessageText', options = options)
	
	def send_message(self, chat_id, text, parse_mode=None, disable_web_page_preview=False, disable_notfication=False, reply_to_message_id = None, reply_markup = None):
		options = {}
		options['chat_id'] = chat_id
		options['text'] = text
		options['disable_notfication'] = disable_notfication
		options['disable_web_page_preview'] = disable_web_page_preview
		
		if parse_mode is not None:
			options['parse_mode'] = parse_mode
		
		if reply_to_message_id is not None:
			options['reply_to_message_id'] = reply_to_message_id
		
		if reply_markup is not None:
			options['reply_markup'] = reply_markup
		
		return self.__api('sendMessage', options=options)
		


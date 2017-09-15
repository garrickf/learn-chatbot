EMOJI_TO_PYTHON = {
	'heart_eyes' : u"\U0001F60D",
	'poop' : u"\U0001F4A9"
}

def emojify(string):
	tokens = string.split()
	for idx, token in enumerate(tokens):
		if token[0] == ':' and token[-1] == ':':
			key = token.replace(':', '')
			print key
			if key in EMOJI_TO_PYTHON:
				print 'found key.'
				tokens[idx] = EMOJI_TO_PYTHON[key]
			else: 
				print 'not found key...'
				tokens[idx] = ''
	print tokens
	#print ' '.join(tokens)
	#return ' '.join(tokens) # join with whitespace character

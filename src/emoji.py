EMOJI_TO_PYTHON = {
	'heart_eyes' : u"\U0001F60D",
	'poop' : u"\U0001F4A9"
} # we want to generate this table

def emojify(string):
	tokens = string.split()
	for idx, token in enumerate(tokens):
		if token[0] == ':' and token[-1] == ':':
			key = token.replace(':', '')
			#print key
			if key in EMOJI_TO_PYTHON: tokens[idx] = EMOJI_TO_PYTHON[key]
			else: tokens[idx] = ''
	# print ' '.join(tokens)
	return ' '.join(tokens) # join with single whitespace character

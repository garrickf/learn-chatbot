from textblob import Word, TextBlob

'''
	print str(parsed.noun_phrases)
	print str(parsed.sentiment)
	

	if noun:
		print '3: tell me more about ' + noun[0] # possible subject: a noun they said
		noun_word = noun[0]
		print Word(noun_word).definitions
		print Word(noun_word).synsets


	if verb:
		verb_word = verb[0]
		if Word(verb_word).lemmatize('v') == 'be':
			print '1: to be' # they used a to be verb
		else:
			print '2: not to be' # they used a different verb
'''

def find_candidate_parts_of_speech(parsed):
	"""Given a parsed input, find the best pronoun, direct noun, adjective, and verb to match their input.
	Returns a tuple of pronoun, noun, adjective, verb any of which may be None if there was no good match"""
	pronoun = None
	noun = None
	adjective = None
	verb = None
	for sent in parsed.sentences:
		pronoun = find_pronoun(sent)
		noun = find_noun(sent)
		adjective = find_adjective(sent)
		verb = find_verb(sent)
	#logger.info("Pronoun=%s, noun=%s, adjective=%s, verb=%s", pronoun, noun, adjective, verb)
	#print 'sig: ', pronoun, noun, adjective, verb
	return pronoun, noun, adjective, verb

def find_pronoun(sent):
	"""Given a sentence, find the likely pronoun of address. Returns None if no candidate
	pronoun is found in the input"""
	pronoun = None

	for word, part_of_speech in sent.pos_tags:
		# Disambiguate pronouns
		if part_of_speech == 'PRP' and word.lower() == 'you':
			pronoun = 'you'
		elif word.lower() == 'i':
			# If the user mentioned themselves, then they will definitely be the pronoun
			pronoun = 'I'
		elif part_of_speech == 'PRP':
			pronoun = word # any other pronoun
	return pronoun

def find_verb(sent):
	"""Pick a candidate verb for the sentence."""
	verb = None
	pos = None
	for word, part_of_speech in sent.pos_tags:
		if part_of_speech.startswith('VB'):  # This is a verb
			verb = word
			pos = part_of_speech
			break
	return verb, pos

def find_noun(sent):
	"""Given a sentence, find the best candidate noun."""
	for w, p in sent.pos_tags:
		if p.startswith('NN'):  # This is a noun
			return w, p

def find_adjective(sent):
	"""Given a sentence, find the best candidate adjective."""
	adj = None
	for w, p in sent.pos_tags:
		if p == 'JJ':  # This is an adjective
			adj = w
			break
	return adj

def determine_sent_type(parsed, verb):
	probs = []
	probs.append(prob_is_imperative(parsed, verb))
	probs.append(prob_is_interrogative(parsed))
	probs.append(prob_is_exclamatory(parsed))
	probs.append(prob_is_declarative(parsed, verb))
	curr_max = .3
	max_idx = 4
	for idx, val in enumerate(probs):
		if val >= curr_max:
			curr_max = val
			max_idx = idx
	return ['imp', 'int', 'exc', 'dec', '?'][max_idx]

def prob_is_imperative(sent, verb):
	certainty = 0
	first = sent.tags[0]
	if first[1] == 'VB' or first[1] == 'VBP': # begins with verb (strong)
		certainty += .9
	if first[1] == 'MD': # begins with modal (med)
		certainty += .5
	if first[0].lower() == 'you' and sent.tags[1][1] == 'MD': # begins with you + modal (med)
		certainty += .6
	if first[0].lower() == 'you': # begins with you (weak)
		certainty += .5 # note: what about weights and conditional probabilities? :)
	if verb is None: # could be misinterpreting the front! (weak)
		certainty += .3
	if sent[-1] == '.': # period (weak)
		certainty += .1
	print 'imp', certainty 
	return certainty

def prob_is_interrogative(sent):
	certainty = 0
	first = sent.tags[0]
	if first[1].startswith('W') : # begins with q-word (strong)
		certainty += .9
	if sent[-1] == '?': # ends with q-mark (strong)
		certainty += .9
	print 'int', certainty 
	return certainty

def prob_is_exclamatory(sent):
	certainty = 0
	first = sent.tags[0]
	if first[1] == 'UH' : # begins with interjection (strong)
		certainty += .9
	if sent[-1] == '!': # ends with !-mark (strong)
		certainty += .9
	for char in sent: # every capital letter counts (med, scaled)
		if char.isupper():
			certainty += .8 / len(sent)
	print 'exc', certainty 
	return certainty

def prob_is_declarative(sent, verb):
	certainty = 0
	first = sent.tags[0]
	if verb[0] is not None: # to be verb (strong)
		certainty += .35
		verb_word = verb[0]
		if Word(verb_word).lemmatize('v') == 'be':
			certainty += .35
	if first[1].startswith('N') or first[1].startswith('P'): # begins with noun (strong)
		certainty += .2
	if sent[-1] == '.': # ends with .
		certainty += .2
	print 'dec', certainty 
	return certainty

def determine_question_type(sent):
	qwords = ['who', 'what', 'where', 'when', 'why', 'how']
	for word in sent.words:
		if word.lower() in qwords:
			return word.lower()
	return 'other'

def is_tobe(verb):
	if verb[0] is not None: # to be verb
		verb_word = verb[0]
		if Word(verb_word).lemmatize('v') == 'be':
			return True
	return False		
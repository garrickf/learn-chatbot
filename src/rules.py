from textblob import Word, TextBlob
from textblob.wordnet import VERB
#import logging

def reply(text):
	cleaned = text # sanitize text?
	parsed = TextBlob(cleaned)
	prob_is_imperative(parsed)
	
	print str(parsed.tags)
	'''
	print str(parsed.noun_phrases)
	print str(parsed.sentiment)
	pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)

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
	return 'finished.'

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
	print 'sig: ', pronoun, noun, adjective, verb
	return pronoun, noun, adjective, verb

def find_pronoun(sent):
	"""Given a sentence, find a preferred pronoun to respond with. Returns None if no candidate
	pronoun is found in the input"""
	pronoun = None

	for word, part_of_speech in sent.pos_tags:
		# Disambiguate pronouns
		if part_of_speech == 'PRP' and word.lower() == 'you':
			pronoun = 'you'
		elif part_of_speech == 'PRP' and word.lower() == 'i':
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

def prob_is_imperative(sent):
	certainty = 0
	first = sent.tags[0]
	if first[1] == 'VB' or first[1] == 'VBP' or first[0].lower() == 'you':
		print 'most likely imperative'
	else:
		print 'didnt catch anything'


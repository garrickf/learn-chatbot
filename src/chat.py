from textblob import TextBlob, Word
from textblob.wordnet import VERB
import random, logging
import rules as sentutil
from keywords import * # keywords to look for
from personality import * # our personality
import emoji # to send back emoji
import requests

from nltk.parse.generate import generate, demo_grammar
from nltk import CFG # unsure if i need these

def post_message(message_text, request_url, sender_id):
	requests.post(request_url,
				  headers={'Content-Type': 'application/json'},
				  json={'recipient': {'id': sender_id},
						'message': {'text': message_text}})

def start_typing(request_url, sender_id):
	requests.post(request_url,
				  headers={'Content-Type': 'application/json'},
				  json={'recipient': {'id': sender_id},
						'sender_action': "typing_on"})

def post_meme(request_url, sender_id):
	requests.post(request_url,
				  headers={'Content-Type': 'application/json'},
				  json={'recipient': {'id': sender_id},
						'message': {
							"attachment":{"type":"image",
								"payload":{
									"url":"https://i.redd.it/perk8gpra4mz.png"
								}
							}
						}})

def chat(text, request_url, sender_id):
	start_typing(request_url, sender_id)
	form_reply(text, request_url, sender_id)
	#post_message(message_text, request_url, sender_id)
	#return respond(cleaned)
	#grammar = CFG.fromstring(demo_grammar)
	#return generate(grammar, n=1)

def form_reply(text, request_url, sender_id):
	cleaned = text # sanitize text?
	parsed = TextBlob(cleaned)

	if check_for_greeting(parsed, request_url, sender_id) is True: pass
	else:
		# check passphrases: next step!

		pronoun, noun, adjective, verb = sentutil.find_candidate_parts_of_speech(parsed)
		sent_type = sentutil.determine_sent_type(parsed, verb)

		if sent_type == 'dec':
			handle_statement(parsed, request_url, sender_id)
		elif sent_type == 'imp':
			handle_command(parsed, request_url, sender_id)
		elif sent_type == 'exc':
			handle_exclamation(parsed, request_url, sender_id)
		elif sent_type == 'int':
			handle_question(parsed, request_url, sender_id)
		elif sent_type == '?':
			post_message(random.choice(NONE_RESPONSES), request_url, sender_id)

def check_for_greeting(sent, request_url, sender_id):
	for word in sent.words:
		if word.lower() in GREETING_KEYWORDS:
			post_message(random.choice(GREETING_RESPONSES), request_url, sender_id)
			return True
	return False

def handle_exclamation(sent, request_url, sender_id):
	case = random.randint(0, 3)

	if case <= 1:
		post_message(random.choice(CANNED_EXCLAMATIONS), request_url, sender_id)
	if case == 2:
		post_message(str(sent), request_url, sender_id)
	if case == 3:
		post_message(str(sent) + '!!!!', request_url, sender_id)

def handle_question(sent, request_url, sender_id):
	pronoun, noun, adjective, verb = sentutil.find_candidate_parts_of_speech(sent)
	
	question_type = sentutil.determine_question_type(sent)
	# tobe = sentutil.is_tobe(verb)

	if question_type == 'who':
		if pronoun == 'I':
			post_message(random.choice(WHO_ABOUT_USER_QUESTION_RESPONSES), request_url, sender_id)
		elif pronoun == 'you':
			post_message(random.choice(WHO_ABOUT_BOT_QUESTION_RESPONSES), request_url, sender_id)
		else:
			post_message(random.choice(WHO_NEUTRAL_QUESTION_RESPONSES), request_url, sender_id)
	elif question_type == 'what':
		if pronoun == 'I':
			post_message(random.choice(WHAT_ABOUT_USER_QUESTION_RESPONSES), request_url, sender_id)
		elif pronoun == 'you':
			post_message(random.choice(WHAT_ABOUT_BOT_QUESTION_RESPONSES), request_url, sender_id)
		else:
			print noun
			if noun is not None and len(Word(noun[0]).definitions) != 0:
				post_message(random.choice(Word(noun[0]).definitions), request_url, sender_id)
			else:
				post_message(random.choice(WHAT_NEUTRAL_QUESTION_RESPONSES), request_url, sender_id)
	elif question_type == 'where':
		if pronoun == 'I':
			post_message(random.choice(WHERE_ABOUT_USER_QUESTION_RESPONSES), request_url, sender_id)
		elif pronoun == 'you':
			post_message(random.choice(WHERE_ABOUT_BOT_QUESTION_RESPONSES), request_url, sender_id)
		else:
			post_message(random.choice(WHERE_NEUTRAL_QUESTION_RESPONSES), request_url, sender_id)
	elif question_type == 'when':
		if pronoun == 'I':
			post_message(random.choice(WHEN_ABOUT_USER_QUESTION_RESPONSES), request_url, sender_id)
		elif pronoun == 'you':
			post_message(random.choice(WHEN_ABOUT_BOT_QUESTION_RESPONSES), request_url, sender_id)
		else:
			post_message(random.choice(WHEN_NEUTRAL_QUESTION_RESPONSES), request_url, sender_id)
	elif question_type == 'why':
		if pronoun == 'I':
			post_message(random.choice(WHY_ABOUT_USER_QUESTION_RESPONSES), request_url, sender_id)
		elif pronoun == 'you':
			post_message(random.choice(WHY_ABOUT_BOT_QUESTION_RESPONSES), request_url, sender_id)
		else:
			post_message(random.choice(WHY_NEUTRAL_QUESTION_RESPONSES), request_url, sender_id)
	elif question_type == 'how':
		if pronoun == 'I':
			post_message(random.choice(HOW_ABOUT_USER_QUESTION_RESPONSES), request_url, sender_id)
		elif pronoun == 'you':
			post_message(random.choice(HOW_ABOUT_BOT_QUESTION_RESPONSES), request_url, sender_id)
		else:
			post_message(random.choice(HOW_NEUTRAL_QUESTION_RESPONSES), request_url, sender_id)
	else:
		post_message(random.choice(CANNED_QUESTION_RESPONSES) + pronoun, request_url, sender_id)

	#case = random.randint(0, 5)

	#if case <= 3:
		#post_message(random.choice(CANNED_QUESTION_RESPONSES), request_url, sender_id)

def handle_command(sent, request_url, sender_id):
	case = random.randint(0, 3)
	pronoun, noun, adjective, verb = sentutil.find_candidate_parts_of_speech(sent)

	if noun is not None and noun[0].lower() == 'meme':
		post_meme(request_url, sender_id)
		post_message('you bingo bonGOED the wrONG PERsoN', request_url, sender_id)

	elif case <= 3:
		post_message(random.choice(CANNED_COMMAND_RESPONSES), request_url, sender_id)

def handle_statement(sent, request_url, sender_id):
	pronoun, noun, adjective, verb = sentutil.find_candidate_parts_of_speech(sent)
	
	case = random.randint(0, 3)

	if case == 0: # can a response sometimes
		post_message(random.choice(CANNED_STATEMENT_RESPONSES), request_url, sender_id)
	if case == 1: # ask to elaborate sometimes
		post_message('huh. tell me more about ' + noun[0], request_url, sender_id)
	if case == 2: # detect polarity sometimes
		polarity = sent.sentiment.polarity
		if polarity < -.1:
			if pronoun == 'I': # directed
				post_message('harrrsh. no need to be hard on yourself bruh', request_url, sender_id)
			elif pronoun == 'you': # self
				post_message('woah mean >:( you are hurting my fragile personailty', request_url, sender_id)
			else:
				post_message('harrrsh', request_url, sender_id)
		elif polarity > .1:
			if pronoun == 'I': # directed
				post_message('yeah...well...im, uh better', request_url, sender_id)
			elif pronoun == 'you': # self
				post_message('dude keep up the compliments!', request_url, sender_id)
			else:
				post_message('aw thats nice', request_url, sender_id)
		else:
			post_message('p neutral man', request_url, sender_id)
	if case == 3: # detect subjectivity sometimes
		subjectivity = sent.sentiment.subjectivity
		print 'sub', subjectivity
		if subjectivity < .15:
			post_message('is that a priori knowlege lol', request_url, sender_id)
		elif subjectivity < .65:
			post_message('ok. maybe a little subjective bro but im here for it', request_url, sender_id)
		else:
			post_message('hold me, the subjectivity lol', request_url, sender_id)








'''Their stuff.'''

# start:example-self.py
# If the user tries to tell us something about ourselves, use one of these responses
COMMENTS_ABOUT_SELF = [
	"You're just jealous",
	"I worked really hard on that",
	"My Klout score is {}".format(random.randint(100, 500)),
]
# end


class UnacceptableUtteranceException(Exception):
	"""Raise this (uncaught) exception if the response was going to trigger our blacklist"""
	pass


def starts_with_vowel(word):
	"""Check for pronoun compability -- 'a' vs. 'an'"""
	return True if word[0] in 'aeiou' else False


def broback(sentence):
	"""Main program loop: select a response for the input sentence and return it"""
	logger.info("Broback: respond to %s", sentence)
	resp = respond(sentence)
	return resp



# start:example-construct-response.py
def construct_response(pronoun, noun, verb):
	"""No special cases matched, so we're going to try to construct a full sentence that uses as much
	of the user's input as possible"""
	resp = []


	if pronoun:
		resp.append(pronoun)

	# We always respond in the present tense, and the pronoun will always either be a passthrough
	# from the user, or 'you' or 'I', in which case we might need to change the tense for some
	# irregular verbs.
	if verb:
		verb_word = verb[0]
		if verb_word in ('be', 'am', 'is', "'m"):  # This would be an excellent place to use lemmas!
			if pronoun.lower() == 'you':
				# The bot will always tell the person they aren't whatever they said they were
				resp.append("aren't really")
			else:
				resp.append(verb_word)
	if noun:
		pronoun = "an" if starts_with_vowel(noun) else "a"
		resp.append(pronoun + " " + noun)

	resp.append(random.choice(("tho", "bro", "lol", "bruh", "smh", "")))

	return " ".join(resp)
# end


# start:example-check-for-self.py
def check_for_comment_about_bot(pronoun, noun, adjective):
	"""Check if the user's input was about the bot itself, in which case try to fashion a response
	that feels right based on their input. Returns the new best sentence, or None."""
	resp = None
	if pronoun == 'I' and (noun or adjective):
		if noun:
			if random.choice((True, False)):
				resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})
			else:
				resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
		else:
			resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})
	return resp

# Template for responses that include a direct noun which is indefinite/uncountable

SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [
	"My last startup totally crushed the {noun} vertical",
	"Were you aware I was a serial entrepreneur in the {noun} sector?",
	"My startup is Uber for {noun}",
	"I really consider myself an expert on {noun}",
]

SELF_VERBS_WITH_NOUN_LOWER = [
	"Yeah but I know a lot about {noun}",
	"My bros always ask me about {noun}",
]

SELF_VERBS_WITH_ADJECTIVE = [
	"I'm personally building the {adjective} Economy",
	"I consider myself to be a {adjective}preneur",
]
# end

def preprocess_text(sentence):
	"""Handle some weird edge cases in parsing, like 'i' needing to be capitalized
	to be correctly identified as a pronoun"""
	cleaned = []
	words = sentence.split(' ')
	for w in words:
		if w == 'i':
			w = 'I'
		if w == "i'm":
			w = "I'm"
		cleaned.append(w)

	return ' '.join(cleaned)

# start:example-respond.py
def respond(sentence):
	"""Parse the user's inbound sentence and find candidate terms that make up a best-fit response"""
	cleaned = preprocess_text(sentence)
	parsed = TextBlob(cleaned)

	# Loop through all the sentences, if more than one. This will help extract the most relevant
	# response text even across multiple sentences (for example if there was no obvious direct noun
	# in one sentence
	pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)

	# If we said something about the bot and used some kind of direct noun, construct the
	# sentence around that, discarding the other candidates
	resp = check_for_comment_about_bot(pronoun, noun, adjective)

	# If we just greeted the bot, we'll use a return greeting
	if not resp:
		resp = check_for_greeting(parsed)

	if not resp:
		# If we didn't override the final sentence, try to construct a new one:
		if not pronoun:
			resp = random.choice(NONE_RESPONSES)
		elif pronoun == 'I' and not verb:
			resp = random.choice(COMMENTS_ABOUT_SELF)
		else:
			resp = construct_response(pronoun, noun, verb)

	# If we got through all that with nothing, use a random response
	if not resp:
		resp = random.choice(NONE_RESPONSES)

	logger.info("Returning phrase '%s'", resp)
	# Check that we're not going to say anything obviously offensive
	filter_response(resp)

	return resp

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
	logger.info("Pronoun=%s, noun=%s, adjective=%s, verb=%s", pronoun, noun, adjective, verb)
	return pronoun, noun, adjective, verb
# end

# start:example-filter.py
def filter_response(resp):
	"""Don't allow any words to match our filter list"""
	tokenized = resp.split(' ')
	for word in tokenized:
		if '@' in word or '#' in word or '!' in word:
			raise UnacceptableUtteranceException()
		for s in FILTER_WORDS:
			if word.lower().startswith(s):
				raise UnacceptableUtteranceException()
# end
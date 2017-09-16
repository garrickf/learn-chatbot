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

def chat(text, request_url, sender_id):
	start_typing(request_url, sender_id)
	message_text = form_reply(text, request_url, sender_id)
	post_message(message_text, request_url, sender_id)
	#return respond(cleaned)
	#grammar = CFG.fromstring(demo_grammar)
  	#return generate(grammar, n=1)

def form_reply(text, request_url, sender_id):
	cleaned = text # sanitize text?
	parsed = TextBlob(cleaned)

	check_for_greeting(parsed, request_url, sender_id)

	pronoun, noun, adjective, verb = sentutil.find_candidate_parts_of_speech(parsed)
	sent_type = sentutil.determine_sent_type(parsed, verb)

	if sent_type == 'dec':
		return 'This is a declarative sentence. I think.'
	elif sent_type == 'imp':
		return 'This is an imperative sentence. You\'re making me do something, I swear!'
	elif sent_type == 'exc':
		return 'This is an exclamatory sentence. Ahh!'
	elif sent_type == 'int':
		return 'This is an interrogative sentence?'
	elif sent_type == '?':
		return 'What was that, again?'




'''Their stuff.'''

def check_for_greeting(sent, request_url, sender_id):
    for word in sent.words:
        if word.lower() in GREETING_KEYWORDS:
            post_message(random.choice(GREETING_RESPONSES), request_url, sender_id)
            return True
	return False

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
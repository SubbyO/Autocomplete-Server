import os
from model import getModel
from utils.helpers import normalizeString
from nltk.tokenize import word_tokenize

'''
  Generate autocomplete suggestions from a given prefix using our data model.
  This function allows clients to specify the maximum number of results that
  are returned and a threshold indicating a minimum number of times each
  result must have occured in the provided data.
'''
def generate_completions(trie, prefix, max_results=None, frequency_threshold=0):
	# Convert prefix to a tuple of lowercase words and strip punctuation
	# So that we can search our model for matching sentences.
	prefix = tuple(word_tokenize(normalizeString(prefix)))
	# We find the node associated with the second to last word in our prefix
	# since the last word may be a fragment (e.g. prefix = 'how ca')
	currentTrie = trie.getnode(prefix[:-1])
	if currentTrie is None:
		return []
	# Get all the word trie nodes that are asociated with our given prefix
	tries = [('', currentTrie)] if not prefix else list(currentTrie.getLetters(prefix[-1]))
	# Obtain every sentence from our data that matches the given prefix
	# and occurs more than frequency_threshold times
	results = dict( ((sentence, count) for _, tr in tries\
		for sentence, count in tr if count > frequency_threshold) )
	# Sort the resulting sentences by their frequencies and only keep the top max_results
	return sorted(results, key = results.__getitem__, reverse=True)[:max_results]

if __name__ == '__main__':
	# Console interface for autocomplete
	datapath = os.path.join(os.path.dirname(__file__), 'sample_conversations.json')
	trie = getModel(datapath)
	print("Type in a prefix to autocomplete",\
		"Use SET_MAX_RESULTS n to set the maximum number of results.",\
		"Use SET_FREQ_THRESHOLD n to set the frequency threshold.",\
		"Type QUIT to exit.")
	max_results, frequency_threshold = None, 0
	while True:
		inp = input("prefix> ").strip()
		if inp == "QUIT":
			break
		elif inp[:16] == 'SET_MAX_RESULTS ':
			try:
				max_results = max(0, int(inp[16:]))
			except:
				print("Error setting max_results to", "'" + inp[16:] + "'.", 'n must be a nonnegative integer.')
		elif inp[:19] == 'SET_FREQ_THRESHOLD ':
			try:
				frequency_threshold = max(0, int(inp[19:]))
			except:
				print("Error setting frequency_threshold to", "'" + inp[19:] + "'.", 'n must be a nonnegative integer.')
		else:
			try:
				results = generate_completions(trie, inp, max_results, frequency_threshold)
				for res in results:
					print(res)
			except Exception as e:
				print("Error autocompleting", inp, ":", e)
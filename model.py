import pandas as pd
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import os.path
import pickle
import sys
from utils.helpers import normalizeString
from utils.trie import WordTrie

def getModel(datapath):
	# Attempt to load in the model from a stored serialized object file
	modelPath = datapath[:datapath.rfind('.')] + '_model.pkl'
	try:
		with open(modelPath, 'rb') as f:
			trie = pickle.load(f)
		print('Loaded data model')
	except:
		# Create a trie with sentences from the provided data if we fail to load the stored model
		print('Creating data model')
		data = pd.read_json(datapath, encoding="utf-8")
		# Select all the messages from the data
		data = pd.DataFrame(data['Issues'].apply(lambda i: i['Messages']))
		# Reformat the data into a table with a row for each sentence seen in the data
		# and two columns; the first corresponding to the 'IsFromCustomer' field,
		# and the other corresponding to the text of each sentence.
		data = pd.concat([pd.DataFrame({'IsFromCustomer': [r['IsFromCustomer']], 'Sentence': [sent]})\
			for _, row in data.iterrows() for r in row[0]\
			for sent in sent_tokenize(r['Text'])]).reset_index()
		del data['index']
		# Select only the sentences that were written by an agent
		# and create a data frame associating these sentences with
		# their frequencies of occurence in the data.
		agentSentences = pd.DataFrame(data[data['IsFromCustomer'] == False].Sentence.value_counts()).reset_index()
		agentSentences.rename(columns={'index': 'Sentence', 'Sentence': 'Count'}, inplace=True)
		# Consolidate equivalent rows by combining sentences that are the same
		# when they are converted to lowercase and stripped of punctuation.
		agentSentences['Normalized'] = agentSentences['Sentence'].apply(normalizeString)
		groupedAgentSentences = agentSentences.groupby(['Normalized'])
		# Keep the form of the sentence that occurs the most in the data when consolidating.
		# We assume that this form is most likely to be correct and thus use it for
		# autocomplete suggestions.
		agentSentences['Count_Max'] = groupedAgentSentences['Count'].transform(max)
		agentSentences['Count_Total'] = groupedAgentSentences['Count'].transform(sum)
		agentSentences = agentSentences[agentSentences['Count'] == agentSentences['Count_Max']]
		agentSentences.drop(['Count', 'Count_Max'], axis=1, inplace=True)
		agentSentences.rename(columns={'Count_Total': 'Count'}, inplace=True)

		# Create our Trie data model that will be used to obtain autocomplete results
		trie = WordTrie()

		'''
		  Add a sentence to our trie data model.
		  Row is a row of a DataFrame with the columns
		  'Sentence', 'Normalized', 'Count'.
		'''
		def addSentence(row, trie):
			sentence, normalized, count = row
			# We split the normalized sentence into a series of word tokens
			# and use these as the keys in our word trie. This way any
			# equivalent sentence (case and punctuation insensitive) that is
			# queried will have this sentence as a result. The original
			# sentence and its frequency is stored as the value in the trie.
			trie[tuple(word_tokenize(normalized))] = (sentence, count)

		# Add every agent sentence from the data to our trie model
		agentSentences.apply(addSentence, args=(trie,), axis=1)

		# Save the serialized data model we generated
		print('Saving data model')
		sys.setrecursionlimit(3000)
		with open(modelPath, 'wb') as f:
			pickle.dump(trie, f, pickle.HIGHEST_PROTOCOL)
	return trie
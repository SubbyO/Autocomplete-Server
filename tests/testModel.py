import unittest
import os, sys
sys.path.append('..')
from model import getModel
from utils.helpers import normalizeString
from nltk.tokenize import word_tokenize

class TestGetModel(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		datapath = os.path.join(os.path.dirname(__file__), 'data', 'test_conversations.json')
		self.model = getModel(datapath)
	
	def testSentences(self):
		'''Test that the model contains all the agent sentences in the dataset and nothing else'''
		agentSentences = {'Hi, how may I help you today?', 'What is your name and account number?',\
			'When can we schedule the delivery?', 'Thanks, have a great day!',\
			'What can I help you with today?', 'When did this occur?'}
		customerSentences = ['Yes, that sounds good.', "I'm having an issue with my router."\
			'4pm would be good for me.', 'Thanks for your help!']
		for sentence, _ in self.model:
			self.assertIn(sentence, agentSentences)
		for sentence in agentSentences:
			self.assertEqual(self.model[tuple(word_tokenize(normalizeString(sentence)))][0],\
				sentence)
		for sentence in customerSentences:
			with self.assertRaises(KeyError):
				self.model[tuple(word_tokenize(normalizeString(sentence)))]
	
	def testCounts(self):
		'''Test that sentences in the model have the correct counts'''
		sentenceCounts = {'Hi, how may I help you today?': 4,\
			'What is your name and account number?': 3,\
			'When can we schedule the delivery?': 1,\
			'Thanks, have a great day!': 2,\
			'What can I help you with today?': 1,\
			'When did this occur?': 1}
		for sentence, count in sentenceCounts.items():
			self.assertEqual(self.model[tuple(word_tokenize(normalizeString(sentence)))][1],\
				count)

	def testCaseAndPunctuationInsensitivity(self):
		'''Test that the model stores sentences as they occured in the data despite the case and punctuation of queries'''
		sentenceVariants = {'hi how may i help you today.': 'Hi, how may I help you today?',\
			'wHaT Is YoUr NaMe AnD aCcOuNt NuMbEr!': 'What is your name and account number?',\
			'W..h!e?n, c.an!! w,e? sch!edu?le. th..e! del?ivery.!,': 'When can we schedule the delivery?',\
			'THANKS HAVE A GREAT DAY': 'Thanks, have a great day!',\
			'What... can I, help you with... today??': 'What can I help you with today?',\
			'!wHEN DID THIS OCCUR!': 'When did this occur?'}
		for variant, sentence in sentenceVariants.items():
			self.assertEqual(self.model[tuple(word_tokenize(normalizeString(variant)))][0],\
				sentence)

if __name__ == '__main__':
	res = unittest.main(verbosity=3, exit=False)
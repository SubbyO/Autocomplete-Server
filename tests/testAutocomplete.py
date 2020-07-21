import unittest
import os, sys
sys.path.append('..')
from model import getModel
from autocomplete import generate_completions

class TestGenerateCompletions(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		datapath = os.path.join(os.path.dirname(__file__), 'data', 'test_conversations.json')
		self.model = getModel(datapath)
	
	def testCorrectCompletions(self):
		'''Test that all correct completions from the data are obtained'''
		expecteds = [{'What is your name and account number?', 'What can I help you with today?'},\
					{'When did this occur?', 'When can we schedule the delivery?'},\
					{'Hi, how may I help you today?'}, {'Thanks, have a great day!'}]
		prefixes = ['What', 'When', 'Hi', 'Thanks']
		results = [set(generate_completions(self.model, prefix)) for prefix in prefixes]
		for i in range(len(expecteds)):
			self.assertSetEqual(results[i], expecteds[i])

	def testCaseAndPunctuationInsensitive(self):
		'''Test that completions are made without sensitivity to the case or punctuation of the prefix'''
		expecteds = [{'What is your name and account number?', 'What can I help you with today?'},\
					{'When did this occur?', 'When can we schedule the delivery?'},\
					{'Hi, how may I help you today?'}, {'Thanks, have a great day!'}]
		prefixes = ['what', 'when', 'hi', 'thanks']
		results = [set(generate_completions(self.model, prefix)) for prefix in prefixes]
		for i in range(len(expecteds)):
			self.assertSetEqual(results[i], expecteds[i])

	def testAbsentPrefix(self):
		'''Test that prefixes that don't show up in the data don't generate any completions'''
		absentPrefixes = ['who', 'how', 'where', 'did', 'hello', 'b']
		results = [generate_completions(self.model, prefix) for prefix in absentPrefixes]
		for result in results:
			self.assertEqual(result, [])

	def testEmptyPrefix(self):
		'''Test that an empty prefix generates every sentence in the data'''
		agentSentences = {'What is your name and account number?', 'What can I help you with today?',\
						  'When did this occur?', 'When can we schedule the delivery?',\
						  'Hi, how may I help you today?', 'Thanks, have a great day!'}
		result = set(generate_completions(self.model, ''))
		self.assertSetEqual(result, agentSentences)

	def testCompletionOrdering(self):
		'''Test that the function returns results in order of most frequent occurence in the data'''
		initialOrder = ['Hi, how may I help you today?',\
						'What is your name and account number?',\
						'Thanks, have a great day!']
		result = generate_completions(self.model, '')
		self.assertEqual(result[:3], initialOrder)

	def testFragmentedWord(self):
		'''Test that a prefix with a fragmented last word generates completions with the fragment'''
		expected = ['What can I help you with today?']
		result = generate_completions(self.model, 'What ca')
		self.assertEqual(result, expected)

	def testMaxResults(self):
		'''Test that when the max_results argument is specified, the function behaves appropriately'''
		topResult = 'What is your name and account number?'
		otherResults = {'What can I help you with today?', 'When did this occur?',\
						'When can we schedule the delivery?'}
		result = generate_completions(self.model, 'Wh', max_results=2)
		self.assertEqual(len(result), 2)
		self.assertEqual(result[0], topResult)
		self.assertIn(result[1], otherResults)

	def testFrequencyThreshold(self):
		'''Test that when the frequency_threshold argument is specified, the function behaves appropriately'''
		expected = ['Hi, how may I help you today?', 'What is your name and account number?',\
					'Thanks, have a great day!']
		result = generate_completions(self.model, '', frequency_threshold=1)
		self.assertEqual(result, expected)

if __name__ == '__main__':
	res = unittest.main(verbosity=3, exit=False)
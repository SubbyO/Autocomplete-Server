from .helpers import strBase, tupleBase

'''
  Parent class for Trie structures
  Tries are recursive trees that allow us to look up word or sentence prefixes efficiently
'''
class Trie:
	def __init__(self, base, value=None):
		self.value = value
		self.children = {}
		self.base = base

	def getnode(self, key):
		if not key:
			return self
		child = self.base(key[0])
		if child in self.children:
			return self.children[child].getnode(key[1:])
		else:
			return None

	def __getitem__(self, key):
		'''
		  Return the value for the specified prefix.  If the given key is not in
		  the trie, raise a KeyError.
		'''
		node = self.getnode(key)
		if node is None:
			raise KeyError
		else:
			return node.value

	def __setitem__(self, key, val):
		'''
		  Set the value for the specified prefix. Key must be an immutable ordered sequence.
		'''
		raise NotImplementedError

	def __delitem__(self, key):
		'''
		  Delete the given key from the trie if it exists.
		'''
		self[key] = None

	def __contains__(self, key):
		'''
		  Returns whether or not key has a value in the Trie.
		'''
		node = self.getnode(key)
		return node is not None and node.value is not None

	def __iter__(self):
		'''
		  Generator of (key, value) pairs for all keys/values in this trie and its children.
		'''
		if self.value is not None:
			yield (self.base(), self.value)
		yield from ((prefix + suffix, val) for prefix in self.children\
			for suffix, val in self.children[prefix])

'''
  Trie in which keys correspond to string prefixes that are partial words.
'''
class LetterTrie(Trie):
	def __init__(self, value=None):
		super().__init__(strBase, value)

	def __setitem__(self, key, value):
		current = self
		for i in key:
			if i not in current.children:
				if value is not None:
					# Add a node for every letter in the prefix we are inserting
					current.children[i] = LetterTrie()
				else:
					# Attempting to delete a key that doesn't exist
					raise KeyError
			current = current.children[i]
		# Update the value of the node corresponding to the prefix given by key
		current.value = value

	def __contains__(self, key):
		'''
		  For letter tries, prefixes that aren't associated with words are
		  still considered to be in the Trie. This allows us to autocomplete
		  queries that end with a fragmented word.
		'''
		return self.getnode(key) is not None

'''
  Trie in which keys correspond to tuple prefixes that are partial sentences.
'''
class WordTrie(Trie):
	def __init__(self, value=None):
		super().__init__(tupleBase, value)
		# The letters field keeps track of the letters
		# that make up the word representend by this node
		self.letters = LetterTrie()

	'''
	  Add a word to the letters trie
	'''
	def addLetters(self, word, trie):
		if word:
			self.letters[word] = trie

	'''
	  Get the node associated with a given prefix in the word represented by this node
	'''
	def getLetters(self, prefix):
		if not prefix or prefix not in self.letters:
			return LetterTrie()
		else:
			return self.letters.getnode(prefix)

	def __setitem__(self, key, value):
		current = self
		for i in key:
			i = self.base(i)
			if i not in current.children:
				if value is not None:
					# Add a node for every word in the prefix we are inserting
					current.children[i] = WordTrie()
					# Associate every prefix of this word with the word's node
					# in the trie so that we can autocomplete word fragments
					current.addLetters(i[0], current.children[i])
				else:
					# Attempting to delete a key that doesn't exist
					raise KeyError
			current = current.children[i]
		current.value = value

	def __iter__(self):
		'''
		  Word tries will store the original sentences in the values of their nodes
		  instead of reconstructing these sentences from the keys of child nodes.
		  This is so that our sentence prefix queries can be case insensitive.
		'''
		if self.value is not None:
			yield self.value
		yield from (val for prefix in self.children for val in self.children[prefix])